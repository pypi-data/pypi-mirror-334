import dataclasses
import logging
import urllib.parse
import torch
import irisml.core
from irisml.tasks.create_azure_computervision_classification_model import AzureComputerVisionModel

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create Azure Computer Vision OCR model.


    Model input is List[Union[PIL.Image.Image, torch.Tensor]]. Output is List[str].

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
        strict (bool): If true, throws an exception on an API failure. Otherwise just logs an exception message.
    """
    VERSION = '0.1.1'

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

        model = AzureComputervisionOcrModel(self.config.endpoint, self.config.api_key, self.config.strict)
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        return self.execute(inputs)


class AzureComputervisionOcrModel(AzureComputerVisionModel):
    def get_url(self, endpoint):
        return urllib.parse.urljoin(endpoint, '/computervision/imageanalysis:analyze?api-version=2023-04-01-preview&features=read')

    def parse_response(self, response_body):
        # TODO: Should we use words/spans?
        return response_body['readResult']['content']

    def collate_result(self, batch):
        return [b if b else '' for b in batch]
