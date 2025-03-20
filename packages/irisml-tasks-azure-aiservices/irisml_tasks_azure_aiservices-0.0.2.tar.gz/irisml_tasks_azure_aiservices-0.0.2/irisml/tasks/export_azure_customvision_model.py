import dataclasses
import hashlib
import logging
import time
import typing
import uuid
import requests
import irisml.core
from irisml.tasks.create_azure_customvision_project import CVSClient

logger = logging.getLogger(__name__)


EXPORT_TYPES = {
        'coreml': ('coreml', None),
        'coreml_fp16': ('coreml', 'coremlfloat16'),
        'dockerfile': ('dockerfile', 'linux'),
        'dockerfile_arm': ('dockerfile', 'arm'),
        'tensorflow': ('tensorflow', None),
        'tensorflow_savedmodel': ('tensorflow', 'tensorflowsavedmodel'),
        'tensorflow_lite': ('tensorflow', 'tensorflowlite'),
        'tensorflow_lite_fp16': ('tensorflow', 'tensorflowlitefloat16'),
        'tensorflow_js': ('tensorflow', 'tensorflowjs'),
        'onnx': ('onnx', None),
        'onnx_fp16': ('onnx', 'onnxfloat16'),
        'openvino': ('openvino', None),
        'openvino_no_postprocess': ('openvino', 'nopostprocess')
        }


class Task(irisml.core.TaskBase):
    """Export a model from an Azure Custom Vision project.

    Config:
        endpoint (str): The endpoint of the Custom Vision service.
        training_key (str): The training key for the Custom Vision service.
        project_id (UUID): The ID of the project to train.
        iteration_id (UUID): The ID of the iteration to export.
        export_type (str): The type of export to perform. One of 'coreml', 'coreml_fp16', 'tensorflow', 'tensorflow_savedmodel', 'tensorflow_lite', 'tensorflow_lite_fp16', 'tensorflow_js',
                            'onnx', 'onnx_fp16', 'openvino', 'openvino_fp16', 'dockerfile', 'dockerfile_arm'.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        endpoint: str
        training_key: str
        project_id: uuid.UUID
        iteration_id: uuid.UUID
        export_type: typing.Literal['coreml', 'coreml_fp16', 'tensorflow', 'tensorflow_savedmodel', 'tensorflow_lite', 'tensorflow_lite_fp16', 'tensorflow_js',
                                    'onnx', 'onnx_fp16', 'openvino', 'openvino_fp16', 'dockerfile', 'dockerfile_arm']

    @dataclasses.dataclass
    class Outputs:
        data: bytes = b''

    def execute(self, inputs):
        platform, flavor = EXPORT_TYPES[self.config.export_type]
        logger.info(f"Exporting model to {platform} with flavor {flavor}")

        client = CVSClient(self.config.endpoint, self.config.training_key)
        params = {'platform': platform}
        if flavor:
            params['flavor'] = flavor

        # Check the current status of the export
        status = 'Exporting'
        url = None

        try:
            status, url = self._get_export_status(client, platform, flavor)
        except RuntimeError:
            logger.debug("Export not found. Will request a new one.")

        if url is None:
            r = client.post(f'/customvision/v3.3/training/projects/{self.config.project_id}/iterations/{self.config.iteration_id}/export', params=params)
            status = r['status']
            logger.info(f"Export requested: {r['status']}")

        while status == 'Exporting':
            time.sleep(3)
            status, url = self._get_export_status(client, platform, flavor)

        if status != 'Done' or url is None:
            raise RuntimeError(f"Export failed: {status} {url}")

        logger.info(f"Downloading model from {url}")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        data = r.content
        file_hash = hashlib.sha1(data).hexdigest()
        logger.info(f"Downloaded {len(data)} bytes. SHA1={file_hash}")
        return self.Outputs(data)

    def _get_export_status(self, client, platform, flavor):
        r = client.get(f'/customvision/v3.3/training/projects/{self.config.project_id}/iterations/{self.config.iteration_id}/export')
        for e in r:
            if e['platform'].lower() == platform and ((e['flavor'] is None and flavor is None) or (e['flavor'] and e['flavor'].lower() == flavor)):
                return e['status'], e['downloadUri']
        raise RuntimeError(f"Export for platform {platform} and flavor {flavor} not found. response={r}")
