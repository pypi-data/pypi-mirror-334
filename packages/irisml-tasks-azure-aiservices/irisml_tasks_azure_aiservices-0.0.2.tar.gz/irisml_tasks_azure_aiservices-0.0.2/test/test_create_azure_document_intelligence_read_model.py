"""
Tests for the create_azure_documentintelligence_read_model task.
"""
import unittest
import unittest.mock
import PIL.Image
import requests
import torch
from irisml.tasks.create_azure_documentintelligence_read_model import Task


class TestCreateAzureDocumentIntelligenceReadModel(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', api_key='12345')).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        mock_post = unittest.mock.Mock()
        mock_post.return_value.headers = {'Operation-Location': 'https://example.com/'}

        mock_get = unittest.mock.Mock()
        analyze_result_values = {
            'apiVersion': 'test',
            'modelId': 'test',
            'stringIndexType': 'test',
            'content': 'test',
            'pages': 'test',
            'paragraphs': 'test',
            'styles': 'test',
            'contentFormat': 'test'
        }
        mock_get.return_value.json.return_value = {
            'status': 'succeeded',
            'analyzeResult': analyze_result_values
        }

        with unittest.mock.patch('requests.Session.get', new=mock_get), \
        unittest.mock.patch('requests.Session.post', new=mock_post):
            model_outputs = outputs.model([PIL.Image.new('RGB', (224, 224)), PIL.Image.new('RGB', (224, 224))])
            self.assertEqual(model_outputs, [analyze_result_values, analyze_result_values])

    def test_error_default_output(self):
        outputs = Task(Task.Config(endpoint='https://example.com/', api_key='12345')).execute(Task.Inputs())
        self.assertIsInstance(outputs.model, torch.nn.Module)

        mock_post = unittest.mock.Mock()
        mock_post.return_value.headers = {'Operation-Location': 'https://example.com/'}
        mock_post.return_value.raise_for_status.side_effect = [None, requests.HTTPError()]

        mock_get = unittest.mock.Mock()
        analyze_result_values = {
            'apiVersion': 'test',
            'modelId': 'test',
            'stringIndexType': 'test',
            'content': 'test',
            'pages': 'test',
            'paragraphs': 'test',
            'styles': 'test',
            'contentFormat': 'test'
        }
        mock_get.return_value.json.return_value = {
            'status': 'succeeded',
            'analyzeResult': analyze_result_values
        }
        mock_get.return_value.raise_for_status.side_effect = [None, requests.HTTPError()]

        with unittest.mock.patch('requests.Session.get', new=mock_get), \
        unittest.mock.patch('requests.Session.post', new=mock_post):
            model_outputs = outputs.model([PIL.Image.new('RGB', (224, 224)), PIL.Image.new('RGB', (224, 224))])
            self.assertEqual(model_outputs, [analyze_result_values, ''])
