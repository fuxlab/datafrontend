from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from categories.models import Category
from projects.models import Project

class TestApiCategories(TestCase):

    def setUp(self):
        self.client = Client()
        self.category_name = 'Categoryname'
        self.project = Project.objects.create(name='Testproject 1')
        self.category = Category.objects.create(name=self.category_name, project=self.project)


    def create_multi(self):
        self.project2 = Project.objects.create(name='Testproject 2')
        self.category2 = Category.objects.create(name=self.category_name + ' 2', project=self.project)
        self.category3 = Category.objects.create(name=self.category_name + ' 3', project=self.project2)
        self.category4 = Category.objects.create(name=self.category_name + ' 4', project=self.project2)


    def test_index(self):    
        response = self.client.get('/api/categories/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.category_name)


    def test_index_filter(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : {'project': self.project.id} })
        response = self.client.get('/api/categories/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.category.id, self.category2.id])


    def test_index_sort_asc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'ASC'] })
        response = self.client.get('/api/categories/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.category_name)


    def test_index_sort_desc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'DESC'] })
        response = self.client.get('/api/categories/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.category4.name)


    def test_index_search(self):
        self.create_multi()

        query_string = urlencode({'filter' : {'q': 'Categoryname 3'}})
        response = self.client.get('/api/categories/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.category3.id)


    def test_creation(self):
        response = self.client.post('/api/categories/', { 'name': self.category_name, 'project': self.project.id })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], self.category_name)


    def test_show(self):
        response = self.client.get('/api/categories/' + str(self.category.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.category_name)


    def test_edit(self):
        response1 = self.client.post('/api/categories/', { 'name': 'old_name', 'project': self.project.id })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 'name': 'new_name', 'project': self.project.id }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/categories/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/categories/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['name'], new_data['name'])


    def test_delete(self):
        response = self.client.delete('/api/categories/' + str(self.category.id) + '/')
        self.assertEqual(response.status_code, 204)
