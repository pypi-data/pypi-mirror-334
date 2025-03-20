import concurrent.futures
import dataclasses
import io
import json
import logging
import time
import typing
import urllib.parse
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient, ContentSettings
import requests
import tenacity
import torch.utils.data
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Train Azure Computer Vision Custom Model.

    This task uploads a dataset to the provided Azure Storage Blob container, trains a custom model using Azure Computer
    Vision API, and deletes the dataset from the container.

    Config:
        endpoint (str): Azure Computer Vision endpoint. Must start with https://.
        api_key (str): Azure Computer Vision API key.
        task_type (str): Task type. Must be one of 'classification_multiclass' or 'object_detection'.
        azure_storage_blob_container_url (str): Azure Storage Blob container URL. Make sure the Computer Vision API resrouce has access to this storage.
        budget_in_hours (int): Budget in hours.
        keep_dataset (bool): Keep the dataset in the container after training.
        model_kind (str): Optional. Model kind. Must be one of 'Generic-Classifier', 'Generic-Detector', or 'Product-Recognizer'.
    """
    VERSION = '0.1.4'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset
        class_names: list[str]
        test_dataset: torch.utils.data.Dataset | None = None

    @dataclasses.dataclass
    class Config:
        endpoint: str
        api_key: str
        task_type: typing.Literal['classification_multiclass', 'object_detection']
        azure_storage_blob_container_url: str
        budget_in_hours: int = 1
        keep_dataset: bool = False
        model_kind: typing.Literal['Generic-Classifier', 'Generic-Detector', 'Product-Recognizer'] | None = None

    @dataclasses.dataclass
    class Outputs:
        model_name: str
        accuracy_top1: float | None = None
        accuracy_top5: float | None = None
        average_precision: float | None = None
        mean_average_precision_30: float | None = None
        mean_average_precision_50: float | None = None
        mean_average_precision_75: float | None = None

    def execute(self, inputs):
        self._uvs_client = UVSClient(self.config.endpoint, self.config.api_key)

        dataset_name = f'dataset_{uuid.uuid4()}'
        test_dataset_name = None
        logger.info(f"Uploading dataset to Azure Storage Blob. {dataset_name=}")
        self._upload_dataset(inputs.dataset, dataset_name, inputs.class_names)

        if inputs.test_dataset:
            test_dataset_name = f'{dataset_name}_test'
            logger.info(f"Uploading test dataset to Azure Storage Blob. {test_dataset_name=}")
            self._upload_dataset(inputs.test_dataset, test_dataset_name, inputs.class_names)

        model_name = f'model_{uuid.uuid4()}'
        logger.info(f"Training model. {model_name=}")
        start = time.time()
        self._train_model(dataset_name, model_name, test_dataset_name)
        logger.info(f"Training model finished. {model_name=}. Elapsed time: {time.time() - start:.2f} seconds")
        if not self.config.keep_dataset:
            logger.info(f"Deleting dataset from Azure Storage Blob...{dataset_name=}")
            self._delete_dataset(dataset_name)
            if test_dataset_name:
                logger.info(f"Deleting test dataset from Azure Storage Blob...{test_dataset_name=}")
                self._delete_dataset(test_dataset_name)

        if test_dataset_name:
            evaluation_result = self._uvs_client.get_model(model_name)['modelPerformance']
            logger.info(f"Evaluation result: {evaluation_result}")
        else:
            evaluation_result = {}

        return self.Outputs(model_name=model_name, accuracy_top1=evaluation_result.get('accuracyTop1'), accuracy_top5=evaluation_result.get('accuracyTop5'),
                            average_precision=evaluation_result.get('averagePrecision'), mean_average_precision_30=evaluation_result.get('meanAveragePrecision30'),
                            mean_average_precision_50=evaluation_result.get('meanAveragePrecision50'), mean_average_precision_75=evaluation_result.get('meanAveragePrecision75'))

    def dry_run(self, inputs):
        return self.Outputs(model_name=str(uuid.uuid4()))

    def _upload_dataset(self, dataset, dataset_name, class_names):
        container_client = ContainerClient.from_container_url(self.config.azure_storage_blob_container_url, credential=DefaultAzureCredential())

        logger.info(f"Uploading {len(dataset)} images to Azure Storage Blob...")
        targets = []
        images = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for i, (image, target) in enumerate(dataset):
                targets.append(target)
                images.append({'id': i + 1, 'width': image.width, 'height': image.height, 'file_name': f'{i}.jpg',
                               'absolute_url': f'{self.config.azure_storage_blob_container_url}/{dataset_name}/{i}.jpg'})
                with io.BytesIO() as f:
                    image.save(f, format='JPEG')
                    image_bytes = f.getvalue()
                executor.submit(self._upload_file, f'{dataset_name}/{i}.jpg', image_bytes, 'image/jpeg', container_client)

        # Construct annotations file
        if self.config.task_type == 'classification_multiclass':
            annotations = [{'id': i + 1, 'image_id': i + 1, 'category_id': int(target) + 1} for i, target in enumerate(targets)]
        elif self.config.task_type == 'object_detection':
            annotation_index = 1
            annotations = []
            for i, target in enumerate(targets):
                for t in target:
                    bbox = [float(t[1]), float(t[2]), float(t[3]) - float(t[1]), float(t[4]) - float(t[2])]
                    annotations.append({'id': annotation_index, 'image_id': i + 1, 'category_id': int(t[0]) + 1, 'bbox': bbox})
                    annotation_index += 1
        else:
            raise ValueError(f"Invalid task_type: {self.config.task_type}")

        # Make dataset json file
        coco_dataset = {'info': {},
                        'categories': [{'id': i + 1, 'name': name} for i, name in enumerate(class_names)],
                        'images': images,
                        'annotations': annotations}

        coco_dataset_json = json.dumps(coco_dataset, indent=2)
        self._upload_file(f'{dataset_name}/dataset.json', coco_dataset_json, 'application/json', container_client)

        json_url = f'{self.config.azure_storage_blob_container_url}/{dataset_name}/dataset.json'
        use_managed_identity = not self._check_public_access(json_url)
        logger.debug(f"The dataset is uploaded to Azure Storage Blob. {json_url=}, {use_managed_identity=}")
        self._uvs_client.register_dataset(dataset_name, self.config.task_type, json_url, use_managed_identity)

    def _delete_dataset(self, dataset_name):
        assert dataset_name
        container_client = ContainerClient.from_container_url(self.config.azure_storage_blob_container_url, credential=DefaultAzureCredential())

        for blob in container_client.list_blobs(name_starts_with=dataset_name):
            container_client.delete_blob(blob)

        self._uvs_client.unregister_dataset(dataset_name)

    def _check_public_access(self, url):
        try:
            response = requests.head(url)
            return response.status_code == 200
        except Exception:
            return False

    def _train_model(self, dataset_name, model_name, test_dataset_name):
        model_kind = self.config.model_kind or {'classification_multiclass': 'Generic-Classifier', 'object_detection': 'Generic-Detector'}[self.config.task_type]
        self._uvs_client.create_model(dataset_name, model_name, model_kind, self.config.budget_in_hours, test_dataset_name)
        logger.info(f"Training request sent. Waiting for training to complete... Training budget is {self.config.budget_in_hours} hours.")
        status = 'notstarted'
        while status in ['notstarted', 'training']:
            time.sleep(60)
            model = self._uvs_client.get_model(model_name)
            status = model['status'].lower()

        if status == 'failed':
            raise RuntimeError(f"Training failed. {model_name=}")
        elif status in ['cancelling', 'cancelled']:
            raise RuntimeError(f"Training cancelled. {model_name=}")

    @tenacity.retry(stop=tenacity.stop_after_attempt(5))
    def _upload_file(self, blob_name, data, content_type, container_client):
        try:
            blob_client = container_client.get_blob_client(blob_name)
            content_settings = ContentSettings(content_type=content_type)
            blob_client.upload_blob(data, content_settings=content_settings, timeout=300, overwrite=False)
        except Exception as e:
            logger.warning(f"Failed to upload {blob_name} to Azure Storage Blob. {e=}")
            raise


def _should_retry(exception):
    if isinstance(exception, requests.exceptions.RequestException):
        response = getattr(exception, 'response', None)
        if response is not None and (response.status_code == 429 or response.status_code >= 500):
            return True
        if isinstance(exception, requests.exceptions.ConnectionError):
            return True
    return False


class UVSClient:
    def __init__(self, endpoint, api_key):
        self._endpoint = endpoint
        if urllib.parse.urlparse(endpoint).path in ('', '/'):
            self._endpoint = urllib.parse.urljoin(self._endpoint, '/computervision/')
        if not self._endpoint.endswith('/'):
            self._endpoint += '/'
        self._headers = {'Ocp-Apim-Subscription-Key': api_key}

    def _get_url(self, path):
        return urllib.parse.urljoin(self._endpoint, path)

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry))
    def register_dataset(self, dataset_name, task_type, file_url, use_managed_identity):
        url = self._get_url(f'datasets/{dataset_name}?api-version=2023-04-01-preview')
        annotation_kind = {'classification_multiclass': 'imageClassification', 'object_detection': 'imageObjectDetection'}[task_type]
        request_body = {'annotationKind': annotation_kind, 'annotationFileUris': [file_url], 'authentication': {'kind': 'managedIdentity' if use_managed_identity else 'none'}}
        response = requests.put(url, headers=self._headers, json=request_body, timeout=60)
        response_json = response.json()
        logger.debug(f"API response: {response_json}")
        response.raise_for_status()

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry))
    def create_model(self, dataset_name, model_name, model_kind, budget_in_hours, test_dataset_name):
        url = self._get_url(f'models/{model_name}?api-version=2023-04-01-preview')
        request_body = {'trainingParameters': {'timeBudgetInHours': budget_in_hours, 'trainingDatasetName': dataset_name, 'modelKind': model_kind}}
        if test_dataset_name:
            request_body['evaluationParameters'] = {'testDatasetName': test_dataset_name}

        response = requests.put(url, headers=self._headers, json=request_body, timeout=60)
        response_json = response.json()
        logger.debug(f"API response: {response_json}")
        response.raise_for_status()

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry))
    def get_model(self, model_name):
        url = self._get_url(f'models/{model_name}?api-version=2023-04-01-preview')
        response = requests.get(url, headers=self._headers, timeout=60)
        response_json = response.json()
        logger.debug(f"API response: {response_json}")
        response.raise_for_status()
        return response_json

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), retry=tenacity.retry_if_exception(_should_retry))
    def unregister_dataset(self, dataset_name):
        url = urllib.parse.urljoin(self._endpoint, f'datasets/{dataset_name}?api-version=2023-04-01-preview')
        response = requests.delete(url, headers=self._headers, timeout=60)
        response.raise_for_status()
