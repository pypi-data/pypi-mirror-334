import atexit
import dataclasses
import hashlib
import io
import logging
import socket
import subprocess
import tempfile
import time
import typing
import zipfile
import requests
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a model from an exported Azure Custom Vision Docker image.

    This task uses 'docker' command to run the exported Docker image. The environment must have Docker installed.

    Config:
        task_type (str): Task type. One of 'classification_multiclass', 'classification_multilabel', 'object_detection'.
        cleanup (bool): Whether to clean up the Docker image after the model is created.
    """
    VERSION = '0.1.1'

    @dataclasses.dataclass
    class Inputs:
        data: bytes
        class_names: list[str]

    @dataclasses.dataclass
    class Config:
        task_type: typing.Literal['classification_multiclass', 'classification_multilabel', 'object_detection']
        cleanup: bool = True

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module

    def execute(self, inputs):
        model_class = {
                'classification_multiclass': CVSDockerClassificationModel,
                'classification_multilabel': CVSDockerClassificationModel,
                'object_detection': CVSDockerObjectDetectionModel,
            }[self.config.task_type]
        model = model_class(inputs.data, self.config.task_type, inputs.class_names, self.config.cleanup)
        return self.Outputs(model=model)

    def dry_run(self, inputs):
        model = torch.nn.Identity()  # Fake
        return self.Outputs(model=model)


class CVSDockerModel(torch.nn.Module):
    def __init__(self, data, task_type, class_names, do_cleanup):
        super().__init__()
        self._data = data
        self._task_type = task_type
        self._class_names = class_names
        self._do_cleanup = do_cleanup
        self._port = self._get_free_port()

        p = subprocess.run(['docker', 'version'], capture_output=True)
        if p.returncode != 0:
            raise RuntimeError(f"docker command is not usable. returncode={p.returncode}, stdout={p.stdout}, stderr={p.stderr}")

        imagetag = 'cvs-' + hashlib.sha1(data).hexdigest()
        logger.info(f"Building docker image... tag={imagetag}")

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(io.BytesIO(data)) as zip_file:
                zip_file.extractall(temp_dir)

            subprocess.run(['docker', 'build', '-t', imagetag, temp_dir], check=True)

        logger.info(f"Built docker image. tag={imagetag}")

        logger.info(f"Starting docker container... port={self._port}")
        p = subprocess.run(['docker', 'run', '-d', '--rm', '-p', f'{self._port}:80', imagetag], check=True, capture_output=True)
        container_id = p.stdout.decode().strip()
        if do_cleanup:
            atexit.register(cleanup, imagetag, container_id)
            logger.info(f"Registered atexit handler for cleanup. tag={imagetag}, container_id={container_id}")
        logger.info(f"Running docker container. container_id={container_id}")
        time.sleep(5)  # Wait for the container to start

    def forward(self, x):
        results = []
        for image in x:
            image_binary = _pil_to_binary(image)
            try:
                r = requests.post(f'http://localhost:{self._port}/image', data=image_binary, timeout=5)
                r.raise_for_status()
                results.append(r.json())
            except Exception as e:
                logger.error(f"Error while requesting to the docker container. {e}")
                results.append(None)

        return self.parse_results(results)

    def parse_results(self, results):
        raise NotImplementedError

    def __getstate__(self):
        return {'data': self._data, 'task_type': self._task_type, 'class_names': self._class_names, 'do_cleanup': self._do_cleanup}

    def __setstate__(self, state):
        self.__init__(state['data'], state['task_type'], state['class_names'], state['do_cleanup'])

    @staticmethod
    def _get_free_port():
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port


class CVSDockerClassificationModel(CVSDockerModel):
    def parse_results(self, results):
        predictions = torch.zeros(len(results), len(self._class_names))
        for i, r in enumerate(results):
            if r is None:
                continue
            for p in r['predictions']:
                try:
                    class_id = self._class_names.index(p['tagName'])
                except ValueError:
                    logger.error(f"Unknown class name: {p['tagName']}")
                    continue
                predictions[i, class_id] = p['probability']
        return predictions


class CVSDockerObjectDetectionModel(CVSDockerModel):
    def parse_results(self, results):
        predictions = []
        for r in results:
            if r is None:
                predictions.append(torch.tensor([], dtype=torch.float32).reshape(-1, 6))
                continue
            boxes = []
            for p in r['predictions']:
                try:
                    class_id = self._class_names.index(p['tagName'])
                except ValueError:
                    logger.error(f"Unknown class name: {p['tagName']}")
                    continue
                boxes.append([class_id, p['probability'], p['boundingBox']['left'], p['boundingBox']['top'],
                              p['boundingBox']['left'] + p['boundingBox']['width'], p['boundingBox']['top'] + p['boundingBox']['height']])
            predictions.append(torch.tensor(boxes, dtype=torch.float32).reshape(-1, 6))
        return predictions


def _pil_to_binary(pil_image):
    with io.BytesIO() as f:
        pil_image.save(f, format='JPEG', quality=95)  # This is lossy.
        return f.getvalue()


def cleanup(imagetag, container_id):
    logger.info(f"Cleaning up... tag={imagetag}, container_id={container_id}")
    subprocess.run(['docker', 'stop', container_id], check=True)
    subprocess.run(['docker', 'rmi', imagetag], check=True)
    logger.info(f"Cleaned up. tag={imagetag}, container_id={container_id}")
