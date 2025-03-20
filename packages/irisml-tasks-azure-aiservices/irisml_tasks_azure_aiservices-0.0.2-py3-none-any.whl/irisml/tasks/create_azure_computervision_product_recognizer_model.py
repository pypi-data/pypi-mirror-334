import dataclasses
import io
import logging
import time
import urllib.parse
import uuid
import PIL.Image
import requests
import tenacity
import torch
import torchvision.transforms.functional
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a model that run inference with a product recognizer model in Azure Computer Vision.

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
        model_name (str): Custom model name to create.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        class_names: list[str]

    @dataclasses.dataclass
    class Config:
        endpoint: str
        api_key: str
        model_name: str

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        if not self.config.endpoint.startswith('https://'):
            raise ValueError('endpoint must start with https://')

        kwargs = {'endpoint': self.config.endpoint, 'api_key': self.config.api_key, 'model_name': self.config.model_name, 'class_names': inputs.class_names}
        model = AzureComputervisionProductRecognizerModel(**kwargs)
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        return self.execute(inputs)


def _should_retry(exception):
    if isinstance(exception, requests.exceptions.RequestException):
        response = getattr(exception, 'response', None)
        if response is not None and (response.status_code == 429 or response.status_code >= 500):
            return True
        if isinstance(exception, requests.exceptions.ConnectionError):
            return True
    return False


class AzureComputervisionProductRecognizerModel(torch.nn.Module):
    def __init__(self, endpoint, api_key, model_name, class_names):
        super().__init__()
        self._endpoint = endpoint
        self._api_key = api_key
        self._model_name = model_name
        self._class_names = class_names
        self._headers = {'Ocp-Apim-Subscription-Key': api_key}

    def forward(self, inputs) -> list:
        results = []
        for image in inputs:
            image_bytes = self._get_image_bytes(image)
            response = None
            try:
                run_id = self._create_run(image_bytes)
                logger.debug(f'Created run {run_id}')
                response = self._wait_and_get_run(run_id)
                self._delete_run(run_id)
            except Exception as e:
                logger.exception(f"Failed to run inference with Azure Computer Vision API {e}")
            results.append(response)

        return [b if b is not None else torch.empty(0, 6, dtype=torch.float32) for b in results]

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry))
    def _create_run(self, image_bytes):
        headers = {'Ocp-Apim-Subscription-Key': self._api_key, 'Content-Type': 'image/png'}
        run_id = str(uuid.uuid4())
        url = urllib.parse.urljoin(self._endpoint, f'/computervision/productrecognition/{self._model_name}/runs/{run_id}?api-version=2023-04-01-preview')
        response = requests.put(url, headers=headers, data=image_bytes)
        response.raise_for_status()
        return run_id

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry))
    def _wait_and_get_run(self, run_id):
        url = urllib.parse.urljoin(self._endpoint, f'/computervision/productrecognition/{self._model_name}/runs/{run_id}?api-version=2023-04-01-preview')
        headers = {'Ocp-Apim-Subscription-Key': self._api_key}
        response_body = {}
        status = 'notstarted'
        while status in ['notstarted', 'running']:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_body = response.json()
            status = response_body['status'].lower()
            time.sleep(1)

        if status == 'succeeded':
            return self._parse_response(response_body)
        else:
            return None

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry))
    def _delete_run(self, run_id):
        url = urllib.parse.urljoin(self._endpoint, f'/computervision/productrecognition/{self._model_name}/runs/{run_id}?api-version=2023-04-01-preview')
        headers = {'Ocp-Apim-Subscription-Key': self._api_key}
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

    def _parse_response(self, response_body):
        if 'result' not in response_body:
            return None

        width = response_body['result']['imageMetadata']['width']
        height = response_body['result']['imageMetadata']['height']
        boxes = response_body['result']['products']
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

    @staticmethod
    def _get_image_bytes(image: PIL.Image.Image | torch.Tensor) -> bytes:
        if isinstance(image, torch.Tensor):
            image = torchvision.transforms.functional.to_pil_image(image)

        if isinstance(image, PIL.Image.Image):
            with io.BytesIO() as f:
                image.save(f, format='PNG')
                return f.getvalue()

        raise TypeError(f"image must be PIL.Image.Image or torch.Tensor, but got {type(image)}")

    def collate_result(self, batch):
        return [b if b else '' for b in batch]
