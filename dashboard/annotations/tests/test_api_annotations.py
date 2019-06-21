from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from projects.models import Project
from categories.models import Category
from datasets.models import Dataset
from images.models import Image
from annotations.models import Annotation

class TestApiAnnotations(TestCase):


    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test 1', project=self.project)
        self.category = Category.objects.create(name='Test Category 1', project=self.project)
        self.image = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)
        self.annotation = Annotation.objects.create(image=self.image, category=self.category)

    def create_multi(self):
        self.category2 = Category.objects.create(name='Test Category 3', project=self.project)
        self.dataset2 = Dataset.objects.create(name='Testdataset 2', project=self.project)
        self.image_with_dataset2 = Image.objects.create(name='img1', url='http://images.com/img2.jpg', dataset=self.dataset2)

        self.annotation2 = Annotation.objects.create(image=self.image, category=self.category2)
        self.annotation3 = Annotation.objects.create(image=self.image_with_dataset2, category=self.category2)
        self.annotation4 = Annotation.objects.create(image=self.image, category=self.category2)


    def test_index(self):
        response = self.client.get('/api/annotations/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['image'], self.image.id)


    def test_index_filter_by_category(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : {'category': self.category.id} })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.annotation.id])


    def test_index_filter_by_dataset(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : {'dataset': self.dataset2.id} })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.annotation3.id])


    def test_index_filter_by_type_annotation(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : { 'type' : 'annotation' } })
        response = self.client.get('/api/annotations/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.annotation.id, self.annotation2.id, self.annotation3.id, self.annotation4.id])


    def test_creation(self):
        response = self.client.post('/api/annotations/', {
            'image': self.image.id,
            'category': self.category.id
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['image'], self.image.id)


    def test_show(self):
        response = self.client.get('/api/annotations/' + str(self.annotation.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['image'], self.image.id)


    def test_edit(self):
        self.create_multi()

        response1 = self.client.post('/api/annotations/', { 'image': self.image.id, 'category': self.category.id })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 'image': self.image.id, 'category': self.category2.id }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/annotations/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/annotations/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['category'], new_data['category'])


    def test_delete(self):
        response = self.client.delete('/api/annotations/' + str(self.annotation.id) + '/')
        self.assertEqual(response.status_code, 204)
