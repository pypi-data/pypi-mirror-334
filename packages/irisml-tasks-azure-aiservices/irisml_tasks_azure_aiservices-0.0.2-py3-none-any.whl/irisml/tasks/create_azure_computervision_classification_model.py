import concurrent.futures
import dataclasses
import io
import logging
import urllib.parse
import PIL.Image
import requests
import tenacity
import torch
import torchvision.transforms.functional
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create Azure Computer Vision Classification Model.

    This task creates a model that assigns tags to an image using Azure Computer Vision API.

    Model input is (image: Union[PIL.Image.Image, torch.Tensor], targets: Any). Output is a list of str.

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
        strict (bool): If true, throws an exception on an API failure. Otherwise just logs an exception message.
    """
    VERSION = '0.1.3'

    @dataclasses.dataclass
    class Config:
        endpoint: str
        api_key: str
        strict: bool = False

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        if not self.config.endpoint.startswith('https://'):
            raise ValueError('endpoint must start with https://')

        model = AzureComputervisionClassificationModel(self.config.endpoint, self.config.api_key, self.config.strict)
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


class AzureComputerVisionModel(torch.nn.Module):
    def __init__(self, endpoint, api_key, strict=False):
        super().__init__()
        self._api_key = api_key
        self._url = self.get_url(endpoint)
        self._pool_executor = concurrent.futures.ThreadPoolExecutor()
        self._http_session = requests.Session()
        self._strict = strict
        self._headers = self.generate_headers(api_key)

    def forward(self, inputs) -> list[str]:
        images_bytes = [self._get_image_bytes(image) for image in inputs]
        responses = self._pool_executor.map(self._request, images_bytes)
        return self.collate_result(responses)

    def get_url(self, endpoint):
        raise NotImplementedError

    def parse_response(self, response_body):
        raise NotImplementedError

    def collate_result(self, batch):
        raise NotImplementedError

    # this is broken out as a separate method to allow subclasses to set their own headers if needed
    @classmethod
    def generate_headers(cls, api_key):
        return {'Ocp-Apim-Subscription-Key': api_key, 'Content-Type': 'image/png'}

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry), wait=tenacity.wait_random(min=0.5, max=3))
    def _request(self, image_bytes):
        response = None
        try:
            response = self._http_session.post(self._url, headers=self._headers, data=image_bytes)
            response.raise_for_status()

            return self.parse_response(response.json())
        except Exception as e:
            # don't create log noise on 429 response
            if not (response is not None and response.status_code == 429):
                response_content = response.content if response is not None else ''
                logger.exception(f"Failed to request to Azure Computer Vision API: {e} {response_content}")

            if self._strict:
                raise
            else:
                return None

    @staticmethod
    def _get_image_bytes(image: PIL.Image.Image | torch.Tensor) -> bytes:
        if isinstance(image, torch.Tensor):
            image = torchvision.transforms.functional.to_pil_image(image)

        if isinstance(image, PIL.Image.Image):
            with io.BytesIO() as f:
                image.save(f, format='PNG')
                return f.getvalue()

        raise TypeError(f"image must be PIL.Image.Image or torch.Tensor, but got {type(image)}")


class AzureComputervisionClassificationModel(AzureComputerVisionModel):
    def get_url(self, endpoint):
        if urllib.parse.urlparse(endpoint).path in ('', '/'):
            endpoint = urllib.parse.urljoin(endpoint, '/computervision/')
        if not endpoint.endswith('/'):
            endpoint += '/'
        return endpoint + 'imageanalysis:analyze?api-version=2023-04-01-preview&features=tags'

    def parse_response(self, response_body):
        return [t['name'] for t in response_body['tagsResult']['values']]

    def collate_result(self, batch):
        return [b if b else [''] for b in batch]
