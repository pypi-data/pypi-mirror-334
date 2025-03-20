import unittest
import unittest.mock
import uuid
from irisml.tasks.export_azure_customvision_model import Task


class TestExportAzureCustomvisionModel(unittest.TestCase):
    def test_simple(self):
        with unittest.mock.patch('irisml.tasks.export_azure_customvision_model.CVSClient') as m_client, unittest.mock.patch('requests.get') as m_get:
            m_instance = m_client.return_value
            m_instance.get.side_effect = [[], [{'platform': 'dockerfile', 'flavor': 'linux', 'status': 'Done', 'downloadUri': 'https://example.com'}]]
            m_instance.post.return_value = {'status': 'Exporting'}
            m_get.return_value.content = b'abc123'
            outputs = Task(Task.Config(endpoint='https://example.com', training_key='abc123',
                                       project_id=uuid.UUID(int=3), iteration_id=uuid.UUID(int=4), export_type='dockerfile')).execute(Task.Inputs())
            self.assertEqual(outputs.data, b'abc123')
            m_instance.post.assert_called_once_with(f'/customvision/v3.3/training/projects/{uuid.UUID(int=3)}/iterations/{uuid.UUID(int=4)}/export',
                                                    params={'platform': 'dockerfile', 'flavor': 'linux'})
