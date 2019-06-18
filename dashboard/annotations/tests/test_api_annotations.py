from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from annotations.models import Annotation

class TestImages(TestCase):


    def setUp(self):
        self.client = Client()
        self.image_id = 1
        self.category_id = 11
        self.annotation = Annotation.objects.create(image_id=self.image_id, category_id=self.category_id)


    def create_multi(self):
        self.annotation2 = Annotation.objects.create(image_id=self.image_id, category_id=11)
        self.annotation3 = Annotation.objects.create(image_id=2, category_id=22)
        self.annotation4 = Annotation.objects.create(image_id=2, category_id=22)


    def test_index(self):
        response = self.client.get('/api/annotations/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['image_id'], self.image_id)


    def test_index_filter(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : {'category_id': 11} })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.annotation.id, self.annotation2.id])


    def test_index_range_first_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 1] })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['image_id'], self.image_id)


    def test_index_range_second_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [1, 2] })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['image_id'], self.annotation2.image_id)


    def test_index_filter_and_range(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 1], 'filter' : {'category_id': 22} })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['image_id'], self.annotation3.image_id)


    def test_index_sort_asc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'ASC'] })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['image_id'], self.image_id)


    def test_index_sort_desc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'DESC'] })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['image_id'], self.annotation4.image_id)


    def test_creation(self):
        response = self.client.post('/api/annotations/', {
            'image_id': self.image_id,
            'category_id': self.category_id
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['image_id'], self.image_id)


    def test_show(self):
        response = self.client.get('/api/annotations/' + str(self.annotation.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['image_id'], self.image_id)


    def test_edit(self):
        response1 = self.client.post('/api/annotations/', { 'image_id': 1, 'category_id': 11 })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 'image_id': 2, 'category_id': 22 }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/annotations/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/annotations/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['image_id'], new_data['image_id'])
        self.assertEqual(response3.data['category_id'], new_data['category_id'])


    def test_delete(self):
        response = self.client.delete('/api/annotations/' + str(self.annotation.id) + '/')
        self.assertEqual(response.status_code, 204)
