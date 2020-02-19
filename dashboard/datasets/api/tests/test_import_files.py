import os
from django.test import TestCase, override_settings, Client
from tests.lib.file_handling import test_create_files, test_delete_folders

from projects.models import Project
from datasets.models import Dataset

from urllib.parse import urlencode
from background_task.models import Task

DATA_PATH = 'datasets/tests/data'

test_settings = override_settings(
    DATAFRONTEND = {
        'DATA_PATH': DATA_PATH
    }
)

class TestImportFiles(TestCase):


    def setUp(self):
        self.client = Client()

        self.project = Project.objects.create(name='Testproject 1')
        self.dataset = Dataset.objects.create(name='Testproject 2', identifier='coco', project=self.project)


    @test_settings
    def test_index_get(self):    
        query_string = urlencode({ 'filter' : {'dataset': self.dataset.id} })
        response = self.client.get('/api/datasets/import_files/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual( [ 'coco_default.json' ], [ file['file_name'] for file in response.data ] )


    @test_settings
    def test_import_file_post(self):
        params = {
            'dataset': self.dataset.id,
            'file_name': 'coco_default.json'
        }
        
        response = self.client.post('/api/datasets/import_files/', params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,{
            'success': True
        })

        # check for new message to init in queue
        tasks = Task.objects.all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task_name, 'datasets.tasks.import_coco.import_coco_task')
