from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from projects.models import Project


class TestProjects(TestCase):

    def setUp(self):
        self.client = Client()
        self.project_name = 'Testproject'
        self.project = Project.objects.create(name=self.project_name)


    def create_multi(self):
        self.project2 = Project.objects.create(name=self.project_name + ' 2')
        self.project3 = Project.objects.create(name=self.project_name + ' 3')
        self.project4 = Project.objects.create(name=self.project_name + ' 4')


    def test_index(self):
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.project_name)


    def test_index_range_first_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 1] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.project_name)


    def test_index_range_second_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [1, 2] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.project2.name)


    def test_index_sort_asc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'ASC'] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.project_name)


    def test_index_sort_desc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'DESC'] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.project4.name)


    def test_index_search(self):
        self.create_multi()

        query_string = urlencode({'filter' : {'q': 'Testproject 3'}})
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.project3.id)


    def test_creation(self):
        c = Client()
        response = self.client.post('/api/projects/', { 'name': self.project_name })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], self.project_name)


    def test_show(self):
        c = Client()
        response = self.client.get('/api/projects/' + str(self.project.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.project_name)


    def test_edit(self):
        c = Client()
        response1 = self.client.post('/api/projects/', { 'name': 'old_name' })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 'name': 'new_name' }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/projects/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/projects/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['name'], new_data['name'])


    def test_delete(self):
        c = Client()
        response = self.client.delete('/api/projects/' + str(self.project.id) + '/')
        self.assertEqual(response.status_code, 204)
