import os

from django.test import TestCase, override_settings, Client
from tests.lib.file_handling import test_create_files, test_delete_folders
from django.test.client import encode_multipart
from urllib.parse import urlencode

from projects.models import Project
from datasets.models import Dataset

from background_task.models import Task

test_settings = override_settings(
    DATAFRONTEND = {
        'DATA_PATH': 'datasets/tests/data/tmp'
    }
)

class TestApiDatasets(TestCase):

    def setUp(self):
        self.client = Client()
        
        self.project = Project.objects.create(name='Project 1')
        self.dataset_name = 'Datasetname'
        self.dataset_identifier = 'identifier'
        self.dataset = Dataset.objects.create(name=self.dataset_name, project=self.project)
        
        self.new_created_folder = os.path.join('datasets/tests/data/tmp', self.dataset_identifier)
        test_create_files([ os.path.join(self.new_created_folder, 'test.txt') ])


    def tearDown(self):
        test_delete_folders([ self.new_created_folder ])


    def create_multi(self):
        self.project2 = Project.objects.create(name='Project 2')
        self.project3 = Project.objects.create(name='Project 3')
        self.project4 = Project.objects.create(name='Project 4')
        self.dataset2 = Dataset.objects.create(name=self.dataset_name + ' 2', project=self.project)
        self.dataset3 = Dataset.objects.create(name=self.dataset_name + ' 3', project=self.project2)
        self.dataset4 = Dataset.objects.create(name=self.dataset_name + ' 4', project=self.project2)


    def test_index(self):    
        response = self.client.get('/api/datasets/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.dataset_name)


    def test_index_filter(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : {'project': self.project.id } })
        response = self.client.get('/api/datasets/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.dataset.id, self.dataset2.id])


    def test_index_sort_asc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'ASC'] })
        response = self.client.get('/api/datasets/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.dataset_name)


    def test_index_sort_desc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'DESC'] })
        response = self.client.get('/api/datasets/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.dataset4.name)


    def test_index_search(self):
        self.create_multi()

        query_string = urlencode({'filter' : {'q': 'Datasetname 3'}})
        response = self.client.get('/api/datasets/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.dataset3.id)


    @test_settings
    def test_creation_existing_folder(self):
        response = self.client.post('/api/datasets/', { 'name': 'new dataset', 'identifier': self.dataset_identifier, 'project': self.project.id })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'new dataset')

        self.assertTrue(os.path.isdir(self.new_created_folder))

        # check for new message to init in queue
        tasks = Task.objects.all()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].task_name, 'datasets.tasks.init_folder.init_folder_task')
        self.assertEqual(tasks[0].params(), ([response.data['id']], {}))


    @test_settings
    def test_creation_new_folder(self):
        response = self.client.post('/api/datasets/', { 'name': 'new dataset', 'identifier': 'new_folder', 'project': self.project.id })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'new dataset')

        # check for new created folder
        expected_created_path = os.path.join('datasets/tests/data/tmp', response.data['identifier'])
        self.assertTrue(os.path.isdir(expected_created_path))
        
        # new folder is created, so no init
        tasks = Task.objects.all()
        self.assertEqual(len(tasks), 0)

        test_delete_folders([ os.path.join('datasets/tests/data/tmp', 'new_folder') ])


    def test_show(self):
        response = self.client.get('/api/datasets/' + str(self.dataset.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.dataset_name)


    def test_edit(self):
        created_id = self.dataset.id

        new_data = { 'name': 'new_name', 'identifier': 'new_identifier', 'project': self.project.id }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/datasets/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/datasets/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['name'], new_data['name'])
        self.assertEqual(response3.data['identifier'], new_data['identifier'])

        # new folder is created, so no init
        tasks = Task.objects.all()
        self.assertEqual(len(tasks), 0)


    def test_delete(self):
        response = self.client.delete('/api/datasets/' + str(self.dataset.id) + '/')
        self.assertEqual(response.status_code, 204)
