from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from categories.models import Category
from datasets.models import Dataset
from images.models import Image
from annotations.models import Annotation, AnnotationBoundingbox

class TestApiAnnotationBoundingboxes(TestCase):


    def setUp(self):
        self.client = Client()
        self.dataset = Dataset.objects.create(name='Test 1')
        self.category = Category.objects.create(name='Test Category 1', dataset=self.dataset)
        self.image = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)
        self.annotation = Annotation.objects.create(image=self.image, category=self.category)
        self.boundingbox = AnnotationBoundingbox.objects.create(
            annotation=self.annotation,
            x_min=100.0,
            x_max=200.0,
            y_min=200.0,
            y_max=300.0,
        )


    def create_multi(self):
        return None


    def test_index(self):
        response = self.client.get('/api/annotation-boundingboxes/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


    def test_index_filter_by_annotation(self):
        query_string = urlencode({ 'filter' : {'annotation': self.annotation.id} })
        response = self.client.get('/api/annotation-boundingboxes/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.boundingbox.id])


    def test_creation_boundingbox(self):
        response = self.client.post('/api/annotation-boundingboxes/', {
             'annotation': self.annotation.id,
             'x_min': 100.0,
             'x_max': 200.0,
             'y_min': 200.0,
             'y_max': 300.0
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['annotation'], self.annotation.id)


    def test_show(self):
        response = self.client.get('/api/annotation-boundingboxes/' + str(self.boundingbox.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.boundingbox.id)


    def test_edit(self):
        self.create_multi()

        response1 = self.client.post('/api/annotation-boundingboxes/', {
            'annotation': self.annotation.id,
            'x_min': 100.0,
            'x_max': 200.0,
            'y_min': 200.0,
            'y_max': 300.0
        })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 
            'annotation': self.annotation.id,
            'x_min': 600.0,
            'x_max': 600.0,
            'y_min': 600.0,
            'y_max': 600.0
        }
        content = encode_multipart('BoUnDaRyStRiNg', new_data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        response2 = self.client.put('/api/annotation-boundingboxes/' + str(created_id) + '/', content, content_type=content_type)

        self.assertEqual(response2.status_code, 200)

        response3 = self.client.get('/api/annotation-boundingboxes/' + str(created_id) + '/')    

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['x_min'], new_data['x_min'])
        self.assertEqual(response3.data['y_max'], new_data['y_max'])


    def test_delete(self):
        response = self.client.delete('/api/annotation-boundingboxes/' + str(self.boundingbox.id) + '/')
        self.assertEqual(response.status_code, 204)
