from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from projects.models import Project
from datasets.models import Dataset
from categories.models import Category
from images.models import Image
from annotations.models import AnnotationSegmentation

class TestApiAnnotationSegmentations(TestCase):


    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test 1', project=self.project)
        self.category = Category.objects.create(name='Test Category 1', project=self.project)
        self.image = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)
        self.segmentation = AnnotationSegmentation.objects.create(
            image=self.image,
            category=self.category,
            width=800,
            height=600,
            mask='emptymask'
        )


    def create_multi(self):
        return None


    def test_index(self):
        response = self.client.get('/api/annotation-segmentations/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


    def test_creation(self):
        response = self.client.post('/api/annotation-segmentations/', {
            'image': self.image.id,
            'category': self.category.id,
            'width': 800,
            'height': 600,
            'mask': 'emptymask'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['image'], self.image.id)


    def test_show(self):
        response = self.client.get('/api/annotation-segmentations/' + str(self.segmentation.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.segmentation.id)


    def test_edit(self):
        self.create_multi()

        response1 = self.client.post('/api/annotation-segmentations/', {
            'image': self.image.id,
            'category': self.category.id,
            'width': 800,
            'height': 600,
            'mask': 'emptymask'
        })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 
            'image': self.image.id,
            'category': self.category.id,
            'width': 1000,
            'height': 2000,
            'mask': 'emptymask'
        }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/annotation-segmentations/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/annotation-segmentations/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['width'], new_data['width'])
        self.assertEqual(response3.data['height'], new_data['height'])


    def test_delete(self):
        response = self.client.delete('/api/annotation-segmentations/' + str(self.segmentation.id) + '/')
        self.assertEqual(response.status_code, 204)
