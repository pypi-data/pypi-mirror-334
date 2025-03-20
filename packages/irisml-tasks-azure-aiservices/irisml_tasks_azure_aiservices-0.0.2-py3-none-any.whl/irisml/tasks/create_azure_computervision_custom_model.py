import dataclasses
import logging
import typing
import urllib.parse
import torch
import irisml.core
from irisml.tasks.create_azure_computervision_classification_model import AzureComputerVisionModel

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a model that run inference with a custom model in Azure Computer Vision.

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
        model_name (str): Custom model name to create.
        task_type (str): Task type. Either 'classification_multiclass' or 'object_detection'.
        strict (bool): If true, throws an exception on an API failure. Otherwise just logs an exception message.
    """
    VERSION = '0.1.4'

    @dataclasses.dataclass
    class Inputs:
        class_names: list[str]

    @dataclasses.dataclass
    class Config:
        endpoint: str
        api_key: str
        model_name: str
        task_type: typing.Literal['classification_multiclass', 'object_detection']
        strict: bool = False

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        if not self.config.endpoint.startswith('https://'):
            raise ValueError('endpoint must start with https://')

        kwargs = {'endpoint': self.config.endpoint, 'api_key': self.config.api_key, 'model_name': self.config.model_name, 'class_names': inputs.class_names, 'strict': self.config.strict}
        if self.config.task_type == 'classification_multiclass':
            model = AzureComputervisionCustomClassificationModel(**kwargs)
        elif self.config.task_type == 'object_detection':
            model = AzureComputervisionCustomObjectDetectionModel(**kwargs)
        else:
            raise ValueError(f'Unknown task_type: {self.config.task_type}')
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        return self.execute(inputs)


class AzureComputervisionCustomModel(AzureComputerVisionModel):
    def __init__(self, *args, model_name, class_names, **kwargs):
        self._model_name = model_name
        self._class_names = class_names
        super().__init__(*args, **kwargs)

    def get_url(self, endpoint):
        if urllib.parse.urlparse(endpoint).path in ('', '/'):
            endpoint = urllib.parse.urljoin(endpoint, '/computervision/')
        if not endpoint.endswith('/'):
            endpoint += '/'
        return endpoint + f'imageanalysis:analyze?api-version=2023-04-01-preview&model-name={self._model_name}'


class AzureComputervisionCustomClassificationModel(AzureComputervisionCustomModel):
    def parse_response(self, response_body):
        predictions = [0] * len(self._class_names)
        if 'tagsResult' not in response_body['customModelResult']:
            return predictions
        tags = response_body['customModelResult']['tagsResult']['values']
        for t in tags:
            predictions[self._class_names.index(t['name'])] = t['confidence']
        return predictions

    def collate_result(self, batch):
        return torch.tensor([b if b is not None else [0] * len(self._class_names) for b in batch])


class AzureComputervisionCustomObjectDetectionModel(AzureComputervisionCustomModel):
    def parse_response(self, response_body):
        if 'objectsResult' not in response_body['customModelResult']:
            return torch.empty(0, 6, dtype=torch.float32)

        width = response_body['metadata']['width']
        height = response_body['metadata']['height']
        boxes = response_body['customModelResult']['objectsResult']['values']
        predictions = []
        for b in boxes:
            x = b['boundingBox']['x'] / width
            y = b['boundingBox']['y'] / height
            w = b['boundingBox']['w'] / width
            h = b['boundingBox']['h'] / height
            box = [x, y, x + w, y + h]
            for t in b['tags']:
                class_index = self._class_names.index(t['name'])
                predictions.append([class_index, t['confidence'], *box])
        return torch.tensor(predictions)

    def collate_result(self, batch):
        return [b if b is not None else torch.empty(0, 6, dtype=torch.float32) for b in batch]
