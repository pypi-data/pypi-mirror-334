import unittest
import unittest.mock

from irisml.tasks.delete_azure_computervision_custom_model import Task


class TestDeleteAzureComputervisionCustomModel(unittest.TestCase):
    def test_simple(self):
        with unittest.mock.patch('requests.delete') as mock_delete:
            Task(Task.Config('https://example.com/', 'fake_key', 'fake_model_name')).execute(Task.Inputs())
            mock_delete.assert_called_once_with('https://example.com/computervision/models/fake_model_name?api-version=2023-04-01-preview',
                                                headers={'Ocp-Apim-Subscription-Key': 'fake_key'}, timeout=unittest.mock.ANY)
