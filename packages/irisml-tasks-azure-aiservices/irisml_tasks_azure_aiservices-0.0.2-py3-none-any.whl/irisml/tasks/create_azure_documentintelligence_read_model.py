"""
Create Azure Document Intelligence Read Model.
"""
import base64
import dataclasses
import json
import logging
import time
import urllib.parse
import tenacity
import torch
import irisml.core
from irisml.tasks.create_azure_computervision_classification_model import _should_retry, AzureComputerVisionModel

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create Azure Document Intelligence Read Model.

    This task creates a model that performs OCR on an image using the Azure Document Intelligence Read service.

    Model input is (image: Union[PIL.Image.Image, torch.Tensor], targets: Any). Output is a list of str.

    Config:
        endpoint (str): Azure Document Intelligence endpoint. Must start with https://.
        api_key (str): Azure Document Intelligence API key.
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

        model = AzureDocumentIntelligenceReadModel(self.config.endpoint, self.config.api_key, self.config.strict)
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        return self.execute(inputs)


class AzureDocumentIntelligenceAnalyzeModel(AzureComputerVisionModel):
    """
    Azure Document Intelligence Analyze Model.
    """
    @classmethod
    def generate_headers(cls, api_key):
        return {"post_request": {'Ocp-Apim-Subscription-Key': api_key, "Content-Type": "application/json"}, "get_request": {'Ocp-Apim-Subscription-Key': api_key}}

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry), wait=tenacity.wait_random(min=0.5, max=3))
    def _request(self, image_bytes):
        data = {
            "base64Source": base64.b64encode(image_bytes).decode('ascii')
        }
        data = json.dumps(data)
        response = None
        try:
            response = self._http_session.post(self._url, headers=self._headers["post_request"], data=data)
            response.raise_for_status()
            analyze_results_url = response.headers['Operation-Location']
            while True:
                response = self._http_session.get(analyze_results_url, headers=self._headers["get_request"])
                response.raise_for_status()
                if response.json()['status'] == 'succeeded':
                    break
                # sleep for 1 second
                time.sleep(1)
            return self.parse_response(response.json())
        except Exception as e:
            # don't create log noise on 429 response
            if not (response is not None and response.status_code == 429):
                response_content = response.content if response is not None else ''
                logger.exception(f"Failed to request to Azure Document Intelligence API: {e} {response_content}")

            if self._strict:
                raise
            else:
                return None

    def parse_response(self, response_body):
        return response_body['analyzeResult']

    def collate_result(self, batch):
        return [b if b else '' for b in batch]

    def get_url(self, endpoint):
        raise NotImplementedError


class AzureDocumentIntelligenceReadModel(AzureDocumentIntelligenceAnalyzeModel):
    """
    Azure Document Intelligence Read Model.
    """
    def get_url(self, endpoint):
        if urllib.parse.urlparse(endpoint).path in ('', '/'):
            endpoint = urllib.parse.urljoin(endpoint, '/documentintelligence/documentModels/')
        if not endpoint.endswith('/'):
            endpoint += '/'
        return endpoint + 'prebuilt-read:analyze?api-version=2024-02-29-preview'
