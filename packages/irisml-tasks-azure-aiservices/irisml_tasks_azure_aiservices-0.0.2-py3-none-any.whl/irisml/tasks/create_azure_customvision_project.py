import dataclasses
import io
import itertools
import logging
import time
import typing
import uuid
import requests
import tenacity
import torch.utils.data
import irisml.core

logger = logging.getLogger(__name__)

DEFAULT_DOMAIN_ID = {
        'classification_multiclass': 'ee85a74c-405e-4adc-bb47-ffa8ca0c9f31',
        'classification_multilabel': 'ee85a74c-405e-4adc-bb47-ffa8ca0c9f31',
        'object_detection': 'da2e3a8a-40a5-4171-82f4-58522f70fbc1'
        }


class Task(irisml.core.TaskBase):
    """Create a new Azure Custom Vision project.

    Note that all images in the dataset will be re-compressed as PNGs.

    Config:
        endpoint: Custom Vision endpoint URL
        training_key: Custom Vision training key
        name: Optional project name. If not specified, a random name will be generated.
        task_type (str): Task type. One of 'classification_multiclass', 'classification_multilabel', 'object_detection'.
        domain_id: Optional domain ID. If not specified, a default domain ID will be used based on the task type.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset
        class_names: list[str]

    @dataclasses.dataclass
    class Config:
        endpoint: str
        training_key: str
        task_type: typing.Literal['classification_multiclass', 'classification_multilabel', 'object_detection']
        name: str | None = None
        domain_id: uuid.UUID | None = None
        use_png: bool = False

    @dataclasses.dataclass
    class Outputs:
        project_id: uuid.UUID = uuid.UUID(int=0)

    def execute(self, inputs):
        logger.info('Creating Azure Custom Vision project')
        if not self.config.use_png:
            logger.info("Images will be re-compressed as JPEGs. To retain original image quality, set 'use_png' to True.")

        client = CVSClient(self.config.endpoint, self.config.training_key)

        # Create project
        params = {'name': self.config.name or f'irisml-{uuid.uuid4()}', 'domainId': self.config.domain_id or DEFAULT_DOMAIN_ID[self.config.task_type]}
        if self.config.task_type == 'classification_multiclass':
            params['classificationType'] = 'multiclass'
        elif self.config.task_type == 'classification_multilabel':
            params['classificationType'] = 'multilabel'

        r = client.post('/customvision/v3.3/training/projects', params)
        project_id = uuid.UUID(r['id'])
        logger.info(f'Created project {project_id}')

        # Create tags
        tags_path = f'/customvision/v3.3/training/projects/{project_id}/tags'
        tag_ids = []
        for class_name in inputs.class_names:
            r = client.post(tags_path, {'name': class_name})
            tag_ids.append(r['id'])
            logger.debug(f'Created tag {r["id"]} for class {class_name}')
            time.sleep(0.1)  # Avoid rate limiting
        logger.info(f"Created {len(inputs.class_names)} tags")

        # Upload images
        for indexes in _batched(range(len(inputs.dataset)), 64):
            _upload_batch_images(client, project_id, inputs.dataset, indexes, self.config.task_type, tag_ids, self.config.use_png)

        # Check the number of uploaded images
        r = client.get(f'/customvision/v3.3/training/projects/{project_id}/images/count', no_json_decode=True)
        image_count = int(r)
        logger.info(f"Uploaded {image_count} images")

        client.close()
        return self.Outputs(project_id=project_id)


def _batched(iterable, batch_size):
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, batch_size))
        if not batch:
            break
        yield batch


def _upload_batch_images(client, project_id, dataset, indexes, task_type, tag_ids, use_png):
    images_path = f'/customvision/v3.3/training/projects/{project_id}/images'

    batch = [dataset[i] for i in indexes]
    batched_images, batched_targets = zip(*batch)

    batched_image_binaries = [_pil_to_binary(img, use_png) for img in batched_images]
    r = client.post(images_path, files={str(i): b for i, b in enumerate(batched_image_binaries)})
    image_ids_by_index = {int(i['sourceUrl'].replace('"', '')): uuid.UUID(i['image']['id']) for i in r['images']}
    image_ids = [image_ids_by_index[i] for i in range(len(batched_images))]

    for image in r['images']:
        if image['status'] == 'OKDuplicate':
            logger.warning(f"Image {image['image']['originalImageUri']} is a duplicate")
        elif image['status'] != 'OK':
            raise RuntimeError(f"Image failed to upload: {image['status']}")

    if task_type == 'classification_multiclass':
        image_tags = set((str(image_id), str(tag_ids[int(target)])) for image_id, target in zip(image_ids, batched_targets))
        data = {'tags': [{'imageId': image_id, 'tagId': tag_id} for image_id, tag_id in image_tags]}
        client.post(f'/customvision/v3.3/training/projects/{project_id}/images/tags', json=data)
    elif task_type == 'classification_multilabel':
        image_tags = set((str(image_id), str(tag_ids[int(t)])) for image_id, targets in zip(image_ids, batched_targets) for t in targets)
        data = {'tags': [{'imageId': image_id, 'tagId': tag_id} for image_id, tag_id in image_tags]}
        client.post(f'/customvision/v3.3/training/projects/{project_id}/images/tags', json=data)
    elif task_type == 'object_detection':
        image_boxes = set((str(image_id), str(tag_ids[int(t[0])]), max(0.0, float(t[1])), max(0.0, float(t[2])),
                           min(1.0, float(t[3])) - max(0.0, float(t[1])), min(1.0, float(t[4])) - max(0.0, float(t[2])))
                          for image_id, targets in zip(image_ids, batched_targets) for t in targets)
        data = [{'imageId': image_id, 'tagId': tag_id, 'left': left, 'top': top, 'width': width, 'height': height}
                for image_id, tag_id, left, top, width, height in image_boxes]
        for data_batch in _batched(data, 64):
            client.post(f'/customvision/v3.3/training/projects/{project_id}/images/regions', json={'regions': data_batch})


def _pil_to_binary(pil_image, use_png: bool):
    with io.BytesIO() as f:
        if use_png:
            pil_image.save(f, format='PNG')
        else:
            pil_image.save(f, format='JPEG', quality=95)
        return f.getvalue()


def _should_retry(exception):
    if isinstance(exception, requests.HTTPError):
        return exception.response.status_code >= 500 or exception.response.status_code == 429
    return True


class CVSClient:
    def __init__(self, endpoint, training_key):
        if endpoint.endswith('/'):
            endpoint = endpoint[:-1]

        self._endpoint = endpoint
        self._session = requests.Session()
        self._session.headers.update({'Training-Key': training_key})

    def close(self):
        self._session.close()

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(5), retry=tenacity.retry_if_exception(_should_retry))
    def get(self, path, params=None, no_json_decode=False):
        url = self._endpoint + path
        logger.debug(f"GET {url} {params=}")
        r = self._session.get(url, params=params, timeout=60)
        CVSClient._check_status(r)
        return r.content if no_json_decode else r.json()

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(5), retry=tenacity.retry_if_exception(_should_retry))
    def post(self, path, params=None, files=None, json=None):
        url = self._endpoint + path
        logger.debug(f"POST {url} {params=} {json=}")
        r = self._session.post(url, params=params, files=files, json=json, timeout=300)  # Longer timeout. Image uploads can take a while
        CVSClient._check_status(r)
        return r.json()

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(5), retry=tenacity.retry_if_exception(_should_retry))
    def patch(self, path, json):
        url = self._endpoint + path
        logger.debug(f"PATCH {url} {json=}")
        r = self._session.patch(url, json=json, timeout=60)
        CVSClient._check_status(r)
        return r.json()

    @tenacity.retry(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(5), retry=tenacity.retry_if_exception(_should_retry))
    def delete(self, path):
        url = self._endpoint + path
        logger.debug(f"DELETE {url}")
        r = self._session.delete(url, timeout=60)
        CVSClient._check_status(r)
        return

    @staticmethod
    def _check_status(response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.warning(f"Request failed with status code {e.response.status_code} and message {e.response.text}")
            raise
