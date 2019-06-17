from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from images.models import Image

class TestImages(TestCase):


    def setUp(self):
        self.client = Client()
        self.image_name = 'Testimage'
        self.image_url = 'http://test.com/image.jpg'
        self.image = Image.objects.create(name=self.image_name, dataset_id=1)


    def create_multi(self):
        self.image2 = Image.objects.create(name=self.image_name + ' 2', dataset_id=1)
        self.image3 = Image.objects.create(name=self.image_name + ' 3', dataset_id=2)
        self.image4 = Image.objects.create(name=self.image_name + ' 4', dataset_id=2)


    def test_index(self):
        response = self.client.get('/api/images/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.image_name)


    def test_index_filter(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : {'dataset_id': 1} })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.image.id, self.image2.id])


    def test_index_range_first_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 1] })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.image_name)


    def test_index_range_second_page(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [1, 2] })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.image2.name)


    def test_index_filter_and_range(self):
        self.create_multi()

        query_string = urlencode({ 'range' : [0, 1], 'filter' : {'dataset_id': 2} })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.image3.name)


    def test_index_sort_asc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'ASC'] })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.image_name)


    def test_index_sort_desc(self):
        self.create_multi()

        query_string = urlencode({'sort' : [ 'id', 'DESC'] })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.image4.name)


    def test_index_search(self):
        self.create_multi()

        query_string = urlencode({'filter' : {'q': 'Testimage 3'}})
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.image3.id)


    def test_creation(self):
        response = self.client.post('/api/images/', {
            'name': self.image_name,
            'url': self.image_url
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], self.image_name)


    def test_show(self):
        response = self.client.get('/api/images/' + str(self.image.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.image_name)


    def test_edit(self):
        response1 = self.client.post('/api/images/', { 'name': 'old_name', 'url': 'http://test.com/image.jpg' })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 'name': 'new_name', 'url': 'http://test.com/new_image.jpg' }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/images/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/images/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['name'], new_data['name'])
        self.assertEqual(response3.data['url'], new_data['url'])


    def test_delete(self):
        response = self.client.delete('/api/images/' + str(self.image.id) + '/')
        self.assertEqual(response.status_code, 204)
