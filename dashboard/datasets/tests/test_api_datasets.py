from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from datasets.models import Dataset


class TestApiDatasets(TestCase):

    def setUp(self):
        self.client = Client()
        self.dataset_name = 'Datasetname'
        self.dataset_identifier = 'Identifier'
        self.dataset = Dataset.objects.create(name=self.dataset_name, project_id=1)


    def create_multi(self):
        self.dataset2 = Dataset.objects.create(name=self.dataset_name + ' 2', project_id=1)
        self.dataset3 = Dataset.objects.create(name=self.dataset_name + ' 3', project_id=2)
        self.dataset4 = Dataset.objects.create(name=self.dataset_name + ' 4', project_id=2)


    def test_index(self):    
        response = self.client.get('/api/datasets/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.dataset_name)


    def test_index_filter(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : {'project_id': 1} })
        response = self.client.get('/api/datasets/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.dataset.id, self.dataset2.id])


    def test_index_range_first_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 1] })
        response = self.client.get('/api/datasets/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.dataset_name)


    def test_index_range_second_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [1, 2] })
        response = self.client.get('/api/datasets/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.dataset2.name)


    def test_index_filter_and_range(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 1], 'filter' : {'project_id': 2} })
        response = self.client.get('/api/datasets/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.dataset3.name)


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


    def test_creation(self):
        response = self.client.post('/api/datasets/', { 'name': self.dataset_name, 'identifier': self.dataset_identifier })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], self.dataset_name)


    def test_show(self):
        response = self.client.get('/api/datasets/' + str(self.dataset.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.dataset_name)


    def test_edit(self):
        response1 = self.client.post('/api/datasets/', { 'name': 'old_name', 'identifier': 'old_identifier' })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 'name': 'new_name', 'identifier': 'new_identifier' }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/datasets/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/datasets/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['name'], new_data['name'])
        self.assertEqual(response3.data['identifier'], new_data['identifier'])


    def test_delete(self):
        response = self.client.delete('/api/datasets/' + str(self.dataset.id) + '/')
        self.assertEqual(response.status_code, 204)
