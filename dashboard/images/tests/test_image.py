from django.test import TestCase, override_settings
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from projects.models import Project
from images.models import Image
from datasets.models import Dataset

from PIL import Image as PImage
from io import BytesIO

test_settings = override_settings(
    DATAFRONTEND = {
        'DATA_PATH': 'images/data/'
    }
)

class TestImages(TestCase):


    def setUp(self):
        self.client = Client()
        self.image_name = 'Testimage'
        self.image_url = 'http://test.com/image.jpg'
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test Dataset 1', identifier='default', project=self.project)
        self.image = Image.objects.create(name='Empty Image', path='default/marmot.jpg', dataset=self.dataset)

    @test_settings
    def test_image_preview(self):
        response = self.client.get('/api/image/' + str(self.image.id) + '.png')
        img = PImage.open(BytesIO(response.content))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(img.size, (299, 169))

    @test_settings
    def test_image_preview_resize(self):
        response = self.client.get('/api/image/' + str(self.image.id) + '.png?resize=500x500')
        img = PImage.open(BytesIO(response.content))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(img.size, (500, 500))

    @test_settings
    def test_image_preview_jpg(self):
        response = self.client.get('/api/image/' + str(self.image.id) + '.jpg')
        img = PImage.open(BytesIO(response.content))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(img.size, (299, 169))
    
    @test_settings
    def test_image_preview_jpg_resize(self):
        response = self.client.get('/api/image/' + str(self.image.id) + '.jpg?resize=500x500')
        img = PImage.open(BytesIO(response.content))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(img.size, (500, 500))


    def test_image_preview_empty(self):
        self.empty_image = Image.objects.create(name='Empty Image', dataset=self.dataset)
        response = self.client.get('/api/image/' + str(self.empty_image.id) + '.png')
        
        self.assertEqual(response.status_code, 404)


    def test_image_preview_not_existent(self):   
        response = self.client.get('/api/image/777.png')
        
        self.assertEqual(response.status_code, 404)
