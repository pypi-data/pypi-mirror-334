import dataclasses
import logging
import urllib.parse
import torch
import irisml.core
from irisml.tasks.create_azure_computervision_classification_model import AzureComputerVisionModel

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create Azure Computer Vision Vectorization Model.

    This task creates a model that vectorizes an image using Azure Computer Vision API.

    Model input is List[Union[PIL.Image.Image, torch.Tensor]]. Output is a List[float].

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
        model_domain (str): Value to use for the 'model-domain' api parameter
        strict (bool): If true, throws an exception on an API failure. Otherwise just logs an exception message.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        endpoint: str
        api_key: str
        model_domain: str = 'generic'
        strict: bool = False

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        if not self.config.endpoint.startswith('https://'):
            raise ValueError('endpoint must start with https://')

        model = AzureComputervisionVectorizationModel(self.config.endpoint, self.config.api_key, self.config.model_domain, self.config.strict)
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        return self.execute(inputs)


class AzureComputervisionVectorizationModel(AzureComputerVisionModel):
    def __init__(self, endpoint, api_key, model_domain, strict):
        self._model_domain = model_domain
        super().__init__(endpoint, api_key, strict)

    def get_url(self, endpoint):
        return urllib.parse.urljoin(endpoint, f'/computervision/retrieval:vectorizeImage?api-version=2023-04-01-preview&model-domain={self._model_domain}')

    def parse_response(self, response_body):
        response = response_body['vector']
        return response

    def collate_result(self, batch):
        return torch.tensor([b if b else [0.0] * 1024 for b in batch])
