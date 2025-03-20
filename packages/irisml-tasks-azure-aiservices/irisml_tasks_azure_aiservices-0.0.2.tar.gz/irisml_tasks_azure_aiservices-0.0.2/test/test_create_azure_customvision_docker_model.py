import io
import unittest
import unittest.mock
import zipfile
import PIL.Image
import torch
from irisml.tasks.create_azure_customvision_docker_model import Task


class TestCreateAzureCustomvisionDockerModel(unittest.TestCase):
    def test_simple(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as zf:
            zf.writestr('app.py', b'abc123')

        data = buf.getvalue()

        with unittest.mock.patch('subprocess.run') as m_run, unittest.mock.patch('requests.post') as m_post:
            m_run.return_value.returncode = 0
            m_post.return_value.json.side_effect = [{'predictions': [{'probability': 0.25, 'tagName': 'cat'}, {'probability': 0.5, 'tagName': 'dog'}]}]
            outputs = Task(Task.Config('classification_multiclass', cleanup=False)).execute(Task.Inputs(data=data, class_names=['cat', 'dog']))
            self.assertIsInstance(outputs.model, torch.nn.Module)

            model_outputs = outputs.model([PIL.Image.new('RGB', (8, 8))])
            self.assertEqual(model_outputs.shape, (1, 2))
            self.assertTrue(torch.allclose(model_outputs, torch.tensor([[0.25, 0.5]])))
