from django.test import TestCase
from django.test import Client
from urllib.parse import urlencode

from projects.models import Project


class TestPagination(TestCase):

    def setUp(self):
        self.client = Client()
        self.project_name = 'Testproject'
        self.project = Project.objects.create(name=self.project_name)


    def create_multi(self):
        self.project2 = Project.objects.create(name=self.project_name + ' 2')
        self.project3 = Project.objects.create(name=self.project_name + ' 3')
        self.project4 = Project.objects.create(name=self.project_name + ' 4')


    def test_index_single(self):
        response = self.client.get('/api/projects/')

        self.assertEqual(response.get('Content-Range'), '0-9/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.project_name)


    def test_index_multi(self):
        self.create_multi()

        response = self.client.get('/api/projects/')

        self.assertEqual(response.get('Content-Range'), '0-9/4')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['name'], self.project_name)


    def test_index_range_first_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 0] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.get('Content-Range'), '0-0/4')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.project.name)


    def test_index_range_second_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [1, 1] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.get('Content-Range'), '1-1/4')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.project2.name)


    def test_index_range_third_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [2, 2] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.get('Content-Range'), '2-2/4')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.project3.name)


    def test_index_range_last_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [3, 3] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.get('Content-Range'), '3-3/4')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.project4.name)


    def test_index_range_first_page_max(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 3] })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.get('Content-Range'), '0-3/4')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data[0]['name'], self.project.name)


    def test_index_max_filter(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : { 'max': 2 } })
        response = self.client.get('/api/projects/?' + query_string)

        self.assertEqual(response.get('Content-Range'), '0-1/4')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
