import os
from django.test import TestCase, override_settings, Client
from tests.lib.file_handling import test_create_files, test_delete_folders

from projects.models import Project
from datasets.models import Dataset

test_settings = override_settings(
    DATAFRONTEND = {
        'DATA_PATH': 'datasets/tests/data/tmp'
    }
)

class TestApiFolders(TestCase):

    def setUp(self):
        self.client = Client()

        test_create_files([
            os.path.join('datasets/tests/data/tmp/folder1', 'file1.txt'),
            os.path.join('datasets/tests/data/tmp/folder2', 'file1.txt')
        ])

        self.project = Project.objects.create(name='Testproject 1')
        self.dataset2 = Dataset.objects.create(name='Testproject 2', identifier='folder2', project=self.project)


    def tearDown(self):
        test_delete_folders(['datasets/tests/data/tmp/folder1', 'datasets/tests/data/tmp/folder2'])
      

    @test_settings
    def test_index(self):    
        response = self.client.get('/api/folders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {
                'id': 'folder1',
                'name': 'folder1'
            }
        ])

