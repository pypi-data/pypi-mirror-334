import unittest
import unittest.mock
import uuid
import PIL.Image
import torch
from irisml.tasks.create_azure_customvision_model import Task


class TestCreateAzureCustomvisionModel(unittest.TestCase):
    def test_image_classification(self):
        with unittest.mock.patch('irisml.tasks.create_azure_customvision_model.CVSClient') as m_client, unittest.mock.patch('requests.Session') as m_session:
            m_instance = m_client.return_value
            m_instance.get.return_value = {'publishName': 'abc123'}

            outputs = Task(Task.Config(endpoint='https://localhost', prediction_endpoint='https://localhost',
                                       training_key='abc123', prediction_key='abc123', prediction_resource_id='fake_resource_id',
                                       project_id=uuid.UUID(int=0), iteration_id=uuid.UUID(int=1), task_type='classification_multiclass')).execute(Task.Inputs(['cat', 'dog']))

            self.assertIsInstance(outputs.model, torch.nn.Module)

            m_session.return_value.post.return_value.json.side_effect = [{'predictions': [{'tagName': 'dog', 'probability': 0.5}, {'tagName': 'cat', 'probability': 0.25}]},
                                                                         {'predictions': [{'tagName': 'dog', 'probability': 0.5}, {'tagName': 'cat', 'probability': 0.25}]}]

            self.assertEqual(outputs.model([PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (100, 100))]).tolist(), [[0.25, 0.5], [0.25, 0.5]])

    def test_object_detection(self):
        with unittest.mock.patch('irisml.tasks.create_azure_customvision_model.CVSClient') as m_client, unittest.mock.patch('requests.Session') as m_session:
            m_instance = m_client.return_value
            m_instance.get.return_value = {'publishName': 'abc123'}

            outputs = Task(Task.Config(endpoint='https://localhost', prediction_endpoint='https://localhost',
                                       training_key='abc123', prediction_key='abc123', prediction_resource_id='fake_resource_id',
                                       project_id=uuid.UUID(int=0), iteration_id=uuid.UUID(int=1), task_type='object_detection')).execute(Task.Inputs(['cat', 'dog']))

            self.assertIsInstance(outputs.model, torch.nn.Module)

            m_session.return_value.post.return_value.json.side_effect = [
                    {'predictions': [{'tagName': 'cat', 'probability': 0.5, 'boundingBox': {'left': 0.1, 'top': 0.1, 'width': 0.2, 'height': 0.2}}]},
                    {'predictions': [{'tagName': 'dog', 'probability': 0.5, 'boundingBox': {'left': 0.1, 'top': 0.1, 'width': 0.2, 'height': 0.3}},
                                     {'tagName': 'cat', 'probability': 0.25, 'boundingBox': {'left': 0.3, 'top': 0.3, 'width': 0.2, 'height': 0.2}}]}]
            model_outputs = outputs.model([PIL.Image.new('RGB', (100, 100)), PIL.Image.new('RGB', (100, 100))])
            self.assertTrue(torch.allclose(model_outputs[0], torch.tensor([[0.0, 0.5, 0.1, 0.1, 0.3, 0.3]])))
            self.assertTrue(torch.allclose(model_outputs[1], torch.tensor([[1.0, 0.5, 0.1, 0.1, 0.3, 0.4], [0.0, 0.25, 0.3, 0.3, 0.5, 0.5]])))
