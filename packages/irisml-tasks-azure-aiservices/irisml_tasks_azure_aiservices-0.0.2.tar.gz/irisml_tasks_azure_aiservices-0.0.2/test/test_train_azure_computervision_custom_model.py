import unittest
import unittest.mock
import PIL.Image
import torch
from irisml.tasks.train_azure_computervision_custom_model import Task


class TestTrainAzureComputervisionCustomModel(unittest.TestCase):
    def test_classification(self):
        dataset = [(PIL.Image.new('RGB', (16, 16)), torch.tensor(0)), (PIL.Image.new('RGB', (16, 16)), torch.tensor(1))]
        class_names = ['class0', 'class1']

        with unittest.mock.patch('irisml.tasks.train_azure_computervision_custom_model.ContainerClient') as mock_container_client, \
             unittest.mock.patch('irisml.tasks.train_azure_computervision_custom_model.requests') as mock_requests, \
             unittest.mock.patch('time.sleep'):
            outputs = Task(Task.Config('https://examle.com/', 'fake_api_key', 'classification_multiclass', 'https://storage.example.com/container')).execute(Task.Inputs(dataset, class_names))
            self.assertTrue(outputs.model_name)
            mock_container_client.from_container_url.assert_called()
            mock_requests.delete.assert_called_once()

    def test_object_detection(self):
        dataset = [(PIL.Image.new('RGB', (16, 16)), torch.tensor([[0, 0, 0, 16, 16]])), (PIL.Image.new('RGB', (16, 16)), torch.tensor([[1, 0, 0, 16, 16]]))]
        class_names = ['class0', 'class1']

        with unittest.mock.patch('irisml.tasks.train_azure_computervision_custom_model.ContainerClient') as mock_container_client, \
                unittest.mock.patch('irisml.tasks.train_azure_computervision_custom_model.requests') as mock_requests, \
                unittest.mock.patch('time.sleep'):
            outputs = Task(Task.Config('https://examle.com/', 'fake_api_key', 'object_detection', 'https://storage.example.com/container')).execute(Task.Inputs(dataset, class_names))
            self.assertTrue(outputs.model_name)
            mock_container_client.from_container_url.assert_called()
            mock_requests.delete.assert_called_once()
