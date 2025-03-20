import dataclasses
import logging
import uuid
import irisml.core
from irisml.tasks.create_azure_customvision_project import CVSClient

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Delete an Azure Custom Vision project

    Config:
        endpoint (str): Azure Custom Vision endpoint
        training_key (str): Azure Custom Vision training key
        project_id (uuid.UUID): Azure Custom Vision project ID
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        endpoint: str
        training_key: str
        project_id: uuid.UUID

    def execute(self, inputs):
        client = CVSClient(self.config.endpoint, self.config.training_key)
        r = client.get(f'/customvision/v3.3/training/projects/{self.config.project_id}/iterations')
        for iteration in r:
            if iteration['publishName']:
                logger.info(f"Iteration {iteration['id']} is published as {iteration['publishName']}, unpublishing")
                client.delete(f'/customvision/v3.3/training/projects/{self.config.project_id}/iterations/{iteration["id"]}/publish')

        client.delete(f'/customvision/v3.3/training/projects/{self.config.project_id}')
        logger.info(f'Deleted project {self.config.project_id}')
        return self.Outputs()
