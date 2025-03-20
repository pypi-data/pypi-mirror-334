import concurrent.futures
import dataclasses
import io
import logging
import typing
import uuid
import requests
import tenacity
import torch
import irisml.core
from irisml.tasks.create_azure_customvision_project import CVSClient

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a prediction model from an Azure Custom Vision project.

    The iteration will be published to the prediction resource. This task doesn't unpublish it, so it will remain published.

    If the iteration was already published, it will be overwritten.

    Config:
        endpoint (str): The endpoint of the Custom Vision service.
        training_key (str): The training key for the Custom Vision service.
        prediction_key (str): The prediction key for the Custom Vision service.
        prediction_resource_id (str): The ID of the prediction resource to publish to.
        project_id (UUID): The ID of the project to train.
        iteration_id (UUID): The ID of the iteration to publish.
        task_type (str): Task type. One of 'classification_multiclass', 'classification_multilabel', 'object_detection'.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        class_names: list[str]

    @dataclasses.dataclass
    class Config:
        endpoint: str
        prediction_endpoint: str
        training_key: str
        prediction_key: str
        prediction_resource_id: str
        project_id: uuid.UUID
        iteration_id: uuid.UUID
        task_type: typing.Literal['classification_multiclass', 'classification_multilabel', 'object_detection']

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        client = CVSClient(self.config.endpoint, self.config.training_key)
        r = client.get(f'/customvision/v3.3/training/projects/{self.config.project_id}/iterations/{self.config.iteration_id}')
        published_name = r['publishName']
        if published_name is not None:
            logger.info(f"Unpublishing iteration {self.config.iteration_id}.")
            client.delete(f'/customvision/v3.3/training/projects/{self.config.project_id}/iterations/{self.config.iteration_id}/publish')

        params = {'publishName': str(self.config.iteration_id), 'predictionId': self.config.prediction_resource_id}
        client.post(f'/customvision/v3.3/training/projects/{self.config.project_id}/iterations/{self.config.iteration_id}/publish', params=params)
        logger.info(f"Published iteration {self.config.iteration_id} to prediction resource {self.config.prediction_resource_id}")

        model_classes = {
                'classification_multiclass': CVSClassificationModel,
                'classification_multilabel': CVSClassificationModel,
                'object_detection': CVSObjectDetectionModel
                }

        model = model_classes[self.config.task_type](self.config.prediction_endpoint, self.config.prediction_key, self.config.project_id, self.config.iteration_id, inputs.class_names)
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        return self.Outputs(model=torch.nn.Module())


def _should_retry(exception):
    if isinstance(exception, requests.HTTPError):
        return exception.response.status_code >= 500 or exception.response.status_code == 429
    return True


class CVSModel(torch.nn.Module):
    def __init__(self, endpoint, prediction_key, project_id, iteraion_name, class_names):
        super().__init__()
        if endpoint.endswith('/'):
            endpoint = endpoint[:-1]

        self._endpoint = endpoint
        self._prediction_key = prediction_key
        self._project_id = project_id
        self._iteration_name = iteraion_name
        self._class_names = class_names
        self._session = requests.Session()
        self._session.headers.update({'Prediction-Key': self._prediction_key, 'Content-Type': 'application/octet-stream'})

    def forward(self, images):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.request_prediction, _pil_to_binary(image)) for image in images]
            results = [f.result() for f in futures]

        return self.aggregate_predictions(results)

    def request_prediction(self, image_binary):
        raise NotImplementedError()

    def aggregate_predictions(self, predictions):
        raise NotImplementedError()

    def __getstate__(self):
        return {'endpoint': self._endpoint, 'prediction_key': self._prediction_key, 'project_id': self._project_id, 'iteration_name': self._iteration_name, 'class_names': self._class_names}

    def __setstate__(self, state):
        self.__init__(state['endpoint'], state['prediction_key'], state['project_id'], state['iteration_name'], state['class_names'])

    @tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(5), retry=tenacity.retry_if_exception(_should_retry))
    def _post(self, prediction_type: typing.Literal['classify', 'detect'], data):
        url = f'{self._endpoint}/customvision/v3.0/prediction/{self._project_id}/{prediction_type}/iterations/{self._iteration_name}/image/nostore'
        r = self._session.post(url, data=data, timeout=60)
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"Error from Custom Vision service: {e.response.text}")
            raise
        return r.json()


class CVSClassificationModel(CVSModel):
    def request_prediction(self, image_binary):
        probs = torch.zeros(len(self._class_names))

        try:
            r = self._post('classify', image_binary)
            for prediction in r['predictions']:
                try:
                    class_id = self._class_names.index(prediction['tagName'])
                except ValueError:
                    logger.error(f"Unknown class name {prediction['tagName']}")
                    continue

                probs[class_id] = prediction['probability']
        except Exception as e:
            logger.error(f"Failed to predict: {e}")

        return probs

    def aggregate_predictions(self, predictions):
        return torch.stack(predictions)


class CVSObjectDetectionModel(CVSModel):
    def request_prediction(self, image_binary):
        boxes = []
        try:
            r = self._post('detect', image_binary)
            for prediction in r['predictions']:
                try:
                    class_id = self._class_names.index(prediction['tagName'])
                except ValueError:
                    logger.error(f"Unknown class name {prediction['tagName']}")
                    continue

                boxes.append([class_id,
                              prediction['probability'],
                              prediction['boundingBox']['left'],
                              prediction['boundingBox']['top'],
                              prediction['boundingBox']['left'] + prediction['boundingBox']['width'],
                              prediction['boundingBox']['top'] + prediction['boundingBox']['height']])

        except Exception as e:
            logger.error(f"Failed to predict: {e}")

        # Reshape to (N, 6) so that it works even if there are no predictions
        return torch.tensor(boxes, dtype=torch.float32).reshape(-1, 6)

    def aggregate_predictions(self, predictions):
        return predictions


def _pil_to_binary(pil_image):
    quality = 95
    while quality > 0:
        with io.BytesIO() as f:
            pil_image.save(f, format='JPEG', quality=quality)  # This is lossy.
            image_binary = f.getvalue()
            if len(image_binary) < 4 * 1024 * 1024:
                return image_binary

        quality -= 5
        logger.warning(f"Image is too large ({len(image_binary)} bytes). Trying lower quality {quality}")
