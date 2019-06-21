from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from projects.models import Project
from images.models import Image
from datasets.models import Dataset

class TestImagePreview(TestCase):


    def setUp(self):
        self.client = Client()
        self.image_name = 'Testimage'
        self.image_url = 'http://test.com/image.jpg'
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test Dataset 1', project=self.project)


    def test_image_preview_empty(self):
        self.empty_image = Image.objects.create(name='Empty Image', dataset=self.dataset)
        
        response = self.client.get('/api/image/' + str(self.empty_image.id) + '.png')
        
        self.assertEqual(response.status_code, 200)


    def test_image_preview_not_existent(self):   
        response = self.client.get('/api/image/777.png')
        
        self.assertEqual(response.status_code, 200)
