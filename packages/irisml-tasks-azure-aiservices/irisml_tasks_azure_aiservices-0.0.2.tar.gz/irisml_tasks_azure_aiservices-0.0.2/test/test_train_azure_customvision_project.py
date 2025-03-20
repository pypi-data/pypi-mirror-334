import unittest
import unittest.mock
import uuid
from irisml.tasks.train_azure_customvision_project import Task


class TestTrainAzureCustomvisionProject(unittest.TestCase):
    def test_classification(self):
        with unittest.mock.patch('irisml.tasks.train_azure_customvision_project.CVSClient') as m_client:
            m_instance = m_client.return_value
            m_instance.get.side_effect = [{'settings': {'domainId': str(uuid.UUID(int=0)), 'classificationType': 'multiclass'}},
                                          {'status': 'Completed', 'trainingTimeInMinutes': 1},
                                          {'performance': None}]
            m_instance.post.return_value = {'id': str(uuid.UUID(int=42))}

            outputs = Task(Task.Config(endpoint='https://localhost/', training_key='fake', task_type='classification_multiclass', project_id=uuid.UUID(int=0))).execute(Task.Inputs())
            self.assertEqual(outputs.iteration_id, uuid.UUID(int=42))
            m_instance.post.assert_called_once()
            m_instance.patch.assert_not_called()

    def test_update_domain(self):
        with unittest.mock.patch('irisml.tasks.train_azure_customvision_project.CVSClient') as m_client:
            m_instance = m_client.return_value
            m_instance.get.side_effect = [{'settings': {'domainId': str(uuid.UUID(int=0)), 'classificationType': 'multiclass'}},
                                          {'status': 'Completed', 'trainingTimeInMinutes': 1},
                                          {'performance': None}]
            m_instance.post.return_value = {'id': str(uuid.UUID(int=42))}

            Task(Task.Config(endpoint='https://localhost/', training_key='fake', task_type='classification_multiclass',
                             project_id=uuid.UUID(int=1), domain_id=uuid.UUID(int=3))).execute(Task.Inputs())
            m_instance.patch.assert_called_once()
