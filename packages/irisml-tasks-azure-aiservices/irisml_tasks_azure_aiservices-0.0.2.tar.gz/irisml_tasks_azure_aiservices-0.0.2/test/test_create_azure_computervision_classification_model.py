import unittest
import unittest.mock
import PIL.Image
import requests
import torch
from irisml.tasks.create_azure_computervision_classification_model import Task


class TestCreateAzureComputervisionClassificationModel(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', api_key='12345')).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        mock_post = unittest.mock.Mock()
        mock_post.return_value.json.return_value = {'tagsResult': {'values': [{'name': 'object_name', 'confidence': 0.5}]}}
        with unittest.mock.patch('requests.Session.post', new=mock_post):
            model_outputs = outputs.model([PIL.Image.new('RGB', (224, 224)), PIL.Image.new('RGB', (224, 224))])
            self.assertEqual(model_outputs, [['object_name'], ['object_name']])

    def test_error_default_output(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', api_key='12345')).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        mock_post = unittest.mock.Mock()
        mock_post.return_value.json.return_value = {'tagsResult': {'values': [{'name': 'object_name', 'confidence': 0.5}]}}
        mock_post.return_value.raise_for_status.side_effect = [None, requests.HTTPError()]
        with unittest.mock.patch('requests.Session.post', new=mock_post):
            model_outputs = outputs.model([PIL.Image.new('RGB', (224, 224)), PIL.Image.new('RGB', (224, 224))])
            self.assertEqual(model_outputs, [['object_name'], ['']])

    def test_error_strict(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', api_key='12345', strict=True)).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        mock_post = unittest.mock.Mock()
        mock_post.return_value.json.return_value = {'tagsResult': {'values': [{'name': 'object_name', 'confidence': 0.5}]}}
        mock_post.return_value.raise_for_status.side_effect = [None, requests.HTTPError()]
        with unittest.mock.patch('requests.Session.post', new=mock_post):
            with self.assertRaises(requests.HTTPError):
                outputs.model([PIL.Image.new('RGB', (224, 224)), PIL.Image.new('RGB', (224, 224))])
