import unittest
import unittest.mock
import uuid
import PIL.Image
import torch
from irisml.tasks.create_azure_customvision_project import Task


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self._data = data

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)


class TestCreateAzureCustomvisionProject(unittest.TestCase):
    def test_image_classification(self):
        dataset = FakeDataset([(PIL.Image.new('RGB', (100, 100)), torch.tensor(0)), (PIL.Image.new('RGB', (100, 100)), torch.tensor(1))])
        class_names = ['cat', 'dog']

        with unittest.mock.patch('irisml.tasks.create_azure_customvision_project.CVSClient') as m_client:
            m_instance = m_client.return_value
            m_instance.post.side_effect = [
                    {'id': str(uuid.UUID(int=0))},
                    {'id': str(uuid.UUID(int=1))},
                    {'id': str(uuid.UUID(int=2))},
                    {'images': [{'sourceUrl': '0', 'status': 'OK', 'image': {'id': str(uuid.UUID(int=3))}}, {'sourceUrl': '1', 'status': 'OK', 'image': {'id': str(uuid.UUID(int=4))}}]},
                    {}]

            m_client.get.return_value = '2'

            m_client.set_post_response('/customvision/v3.3/training/projects', {'id': str(uuid.UUID(int=0))})
            outputs = Task(Task.Config(endpoint='https://example.com', training_key='abc123', task_type='classification_multiclass')).execute(Task.Inputs(dataset, class_names))

            self.assertEqual(outputs.project_id, uuid.UUID(int=0))

    def test_object_detection(self):
        dataset = FakeDataset([(PIL.Image.new('RGB', (100, 100)), torch.tensor([[0, 0, 0, 1, 1]])), (PIL.Image.new('RGB', (100, 100)), torch.tensor([[1, 0, 0, 0.5, 0.5], [1, 0.1, 0.1, 0.3, 0.3]]))])
        class_names = ['cat', 'dog']

        with unittest.mock.patch('irisml.tasks.create_azure_customvision_project.CVSClient') as m_client:
            m_instance = m_client.return_value
            m_instance.post.side_effect = [
                    {'id': str(uuid.UUID(int=0))},
                    {'id': str(uuid.UUID(int=1))},
                    {'id': str(uuid.UUID(int=2))},
                    {'images': [{'sourceUrl': '0', 'status': 'OK', 'image': {'id': str(uuid.UUID(int=3))}}, {'sourceUrl': '1', 'status': 'OK', 'image': {'id': str(uuid.UUID(int=4))}}]},
                    {}]

            m_client.get.return_value = '2'

            m_client.set_post_response('/customvision/v3.3/training/projects', {'id': str(uuid.UUID(int=0))})
            outputs = Task(Task.Config(endpoint='https://example.com', training_key='abc123', task_type='object_detection')).execute(Task.Inputs(dataset, class_names))

            self.assertEqual(outputs.project_id, uuid.UUID(int=0))
