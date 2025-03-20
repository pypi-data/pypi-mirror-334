import unittest
import unittest.mock
import uuid
from irisml.tasks.delete_azure_customvision_project import Task


class TestDeleteAzureCustomvisionProject(unittest.TestCase):
    def test_simple(self):
        with unittest.mock.patch('irisml.tasks.delete_azure_customvision_project.CVSClient') as m_client:
            m_instance = m_client.return_value
            m_instance.get.return_value = [{'publishName': None}]

            Task(Task.Config(endpoint='https://example.com', training_key='abc123', project_id=uuid.UUID(int=3))).execute(Task.Inputs())

            m_instance.delete.assert_called_once_with(f'/customvision/v3.3/training/projects/{uuid.UUID(int=3)}')

    def test_published(self):
        with unittest.mock.patch('irisml.tasks.delete_azure_customvision_project.CVSClient') as m_client:
            m_instance = m_client.return_value
            m_instance.get.return_value = [{'publishName': 'test', 'id': 'fake_id'}]

            Task(Task.Config(endpoint='https://example.com', training_key='abc123', project_id=uuid.UUID(int=3))).execute(Task.Inputs())

            self.assertEqual(m_instance.delete.call_count, 2)
