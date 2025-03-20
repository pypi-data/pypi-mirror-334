import unittest
import unittest.mock
import PIL.Image
import torch
from irisml.tasks.create_azure_computervision_custom_model import Task


class TestCreateAzureComputervisionCustomModel(unittest.TestCase):
    def test_classification(self):
        model_outputs = self._run_task('classification_multiclass', ['label0', 'label1'], [
                {'customModelResult': {'tagsResult': {'values': [{'name': 'label0', 'confidence': 0.25}]}}},
                {'customModelResult': {'tagsResult': {'values': [{'name': 'label1', 'confidence': 0.5}]}}}
                ], [PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (128, 128))])

        self.assertEqual(model_outputs.shape, torch.Size([2, 2]))
        self.assertEqual(model_outputs.tolist(), [[0.25, 0.0], [0.0, 0.5]])

    def test_object_detection(self):
        model_outputs = self._run_task('object_detection', ['label0', 'label1'], [
            {'metadata': {'width': 100, 'height': 100},
                'customModelResult': {'objectsResult': {'values': [{'boundingBox': {'x': 0, 'y': 0, 'w': 100, 'h': 100}, 'tags': [{'name': 'label0', 'confidence': 0.25}]}]}}},
            {'metadata': {'width': 200, 'height': 200},
                'customModelResult': {'objectsResult': {'values': [{'boundingBox': {'x': 0, 'y': 0, 'w': 100, 'h': 100}, 'tags': [{'name': 'label1', 'confidence': 0.5}]}]}}}
            ], [PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (200, 200))])

        self.assertEqual(len(model_outputs), 2)
        self.assertEqual(model_outputs[0].tolist(), [[0, 0.25, 0, 0, 1, 1]])
        self.assertEqual(model_outputs[1].tolist(), [[1, 0.5, 0, 0, 0.5, 0.5]])

    def test_classification_with_error(self):
        model_outputs = self._run_task('classification_multiclass', ['label0', 'label1'], [
            {'customModelResult': {'tagsResult': {'values': [{'name': 'label0', 'confidence': 0.25}]}}},
            RuntimeError('fake error')],
            [PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (128, 128))])

        self.assertEqual(model_outputs.shape, torch.Size([2, 2]))
        self.assertEqual(model_outputs.tolist(), [[0.25, 0.0], [0.0, 0.0]])

    def test_object_detection_with_error(self):
        model_outputs = self._run_task('object_detection', ['label0', 'label1'], [
            {'metadata': {'width': 100, 'height': 100},
                'customModelResult': {'objectsResult': {'values': [{'boundingBox': {'x': 0, 'y': 0, 'w': 100, 'h': 100}, 'tags': [{'name': 'label0', 'confidence': 0.25}]}]}}},
            RuntimeError('fake error')],
            [PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (200, 200))])

        self.assertEqual(len(model_outputs), 2)
        self.assertEqual(model_outputs[0].tolist(), [[0, 0.25, 0, 0, 1, 1]])
        self.assertEqual(model_outputs[1].shape, torch.Size([0, 6]))

    def _run_task(self, task_type, class_names, responses, inputs):
        outputs = Task(Task.Config('https://example.com/', 'fake_api_key', 'fake_model_name', task_type)).execute(Task.Inputs(class_names))
        self.assertIsInstance(outputs.model, torch.nn.Module)
        model = outputs.model

        mock_post = unittest.mock.Mock()
        mock_post.return_value.json.side_effect = responses
        with unittest.mock.patch('requests.Session.post', new=mock_post):
            return model(inputs)
