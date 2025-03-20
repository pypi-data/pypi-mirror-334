import dataclasses
import logging
import time
import typing
import uuid
import irisml.core
from irisml.tasks.create_azure_customvision_project import CVSClient

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Train an Azure Custom Vision project.

    Config:
        endpoint (str): The endpoint of the Custom Vision service.
        training_key (str): The training key for the Custom Vision service.
        project_id (UUID): The ID of the project to train.
        domain_id (Optional[UUID]): The ID of the domain to use for training. If not specified, the project's current domain will be used.
        task_type (Optional['classification_multiclass', 'classification_multilabel', 'object_detection']): The type of task to train for.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        endpoint: str
        training_key: str
        project_id: uuid.UUID
        domain_id: uuid.UUID | None = None
        task_type: typing.Literal['classification_multiclass', 'classification_multilabel', 'object_detection'] | None = None

    @dataclasses.dataclass
    class Outputs:
        iteration_id: uuid.UUID = uuid.UUID(int=0)

    def execute(self, inputs):
        client = CVSClient(self.config.endpoint, self.config.training_key)
        project_path = f'/customvision/v3.3/training/projects/{self.config.project_id}'
        config = client.get(project_path)
        updated = False
        if self.config.domain_id and config['settings']['domainId'] != str(self.config.domain_id):
            config['settings']['domainId'] = str(self.config.domain_id)
            updated = True
        if self.config.task_type == 'classification_multiclass' and config['settings']['classificationType'] != 'multiclass':
            assert config['settings']['classificationType'] == 'multilabel'
            config['settings']['classificationType'] = 'multiclass'
            updated = True
        elif self.config.task_type == 'classification_multilabel' and config['settings']['classificationType'] != 'multilabel':
            assert config['settings']['classificationType'] == 'multiclass'
            config['settings']['classificationType'] = 'multilabel'
            updated = True

        if updated:
            client.patch(project_path, json=config)
            logger.info(f"Updated project {self.config.project_id} with domain {self.config.domain_id} and task type {self.config.task_type}")

        r = client.post(f'{project_path}/train', params={'forceTrain': True})
        iteration_id = uuid.UUID(r['id'])
        logger.info(f"Started training iteration {iteration_id}")
        start_time = time.time()

        iteration_path = f'{project_path}/iterations/{iteration_id}'
        r = client.get(iteration_path)
        status = r['status']

        while status == 'Training':
            time.sleep(60)
            r = client.get(iteration_path)
            status = r['status']
            logger.debug(f"Training iteration {iteration_id} status: {r['status']}")

        elapsed = time.time() - start_time
        logger.info(f"Training iteration {iteration_id} completed in {elapsed} seconds. Status: {status}, training time: {r['trainingTimeInMinutes']} min")

        r = client.get(f'{iteration_path}/performance')
        logger.info(f"Training iteration {iteration_id} performance: {r}")

        return self.Outputs(iteration_id=iteration_id)
