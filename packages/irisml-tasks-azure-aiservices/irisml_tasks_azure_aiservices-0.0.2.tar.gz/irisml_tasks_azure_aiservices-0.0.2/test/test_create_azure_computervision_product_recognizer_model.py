import unittest
import unittest.mock
import PIL.Image
import torch
from irisml.tasks.create_azure_computervision_product_recognizer_model import Task


class TestCreateAzureComputervisionProductRecognizerModel(unittest.TestCase):
    def test_object_detection(self):
        model_outputs = self._run_task(['label0', 'label1'], [
            {'status': 'succeeded', 'result': {'imageMetadata': {'width': 100, 'height': 100},
                                               'products': [{'boundingBox': {'x': 0, 'y': 0, 'w': 100, 'h': 100}, 'tags': [{'name': 'label0', 'confidence': 0.25}]}]}},
            {'status': 'succeeded', 'result': {'imageMetadata': {'width': 200, 'height': 200},
                                               'products': [{'boundingBox': {'x': 0, 'y': 0, 'w': 100, 'h': 100}, 'tags': [{'name': 'label1', 'confidence': 0.5}]}]}}
            ], [PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (200, 200))])

        self.assertEqual(len(model_outputs), 2)
        self.assertEqual(model_outputs[0].tolist(), [[0, 0.25, 0, 0, 1, 1]])
        self.assertEqual(model_outputs[1].tolist(), [[1, 0.5, 0, 0, 0.5, 0.5]])

    def test_object_detection_with_error(self):
        model_outputs = self._run_task(['label0', 'label1'], [
            {'status': 'succeeded', 'result': {'imageMetadata': {'width': 100, 'height': 100},
                                               'products': [{'boundingBox': {'x': 0, 'y': 0, 'w': 100, 'h': 100}, 'tags': [{'name': 'label0', 'confidence': 0.25}]}]}},
            RuntimeError('fake error')],
            [PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (200, 200))])

        self.assertEqual(len(model_outputs), 2)
        self.assertEqual(model_outputs[0].tolist(), [[0, 0.25, 0, 0, 1, 1]])
        self.assertEqual(model_outputs[1].shape, torch.Size([0, 6]))

    def _run_task(self, class_names, responses, inputs):
        outputs = Task(Task.Config('https://example.com/', 'fake_api_key', 'fake_model_name')).execute(Task.Inputs(class_names))
        self.assertIsInstance(outputs.model, torch.nn.Module)
        model = outputs.model

        with unittest.mock.patch('requests.put'), unittest.mock.patch('requests.get') as mock_get, unittest.mock.patch('requests.delete'):
            mock_get.return_value.json.side_effect = responses
            return model(inputs)
