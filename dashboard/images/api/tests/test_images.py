from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from projects.models import Project
from categories.models import Category
from images.models import Image
from datasets.models import Dataset

from annotations.models import Annotation

class TestImagesApi(TestCase):


    def setUp(self):
        self.client = Client()
        self.image_name = 'Testimage'
        self.image_url = 'http://test.com/image.jpg'
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test Dataset 1', project=self.project)
        self.image = Image.objects.create(name=self.image_name, dataset=self.dataset)


    def create_multi(self):
        self.dataset2 = Dataset.objects.create(name='Test Dataset 2', project=self.project)
        self.image2 = Image.objects.create(name=self.image_name + ' 2', dataset=self.dataset)
        self.image3 = Image.objects.create(name=self.image_name + ' 3', dataset=self.dataset2)
        self.image4 = Image.objects.create(name=self.image_name + ' 4', dataset=self.dataset2)


    def test_index(self):
        response = self.client.get('/api/images/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.image_name)


    def test_index_filter(self):
        self.create_multi()

        query_string = urlencode({ 'filter' : {'dataset': self.dataset.id} })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.image.id, self.image2.id])


    def xtest_index_filter_annotation_type(self):
        self.create_multi()

        category1 = Category.objects.create(project=self.project, name='Category 1')
        category2 = Category.objects.create(project=self.project, name='Category 2')
        category3 = Category.objects.create(project=self.project, name='Category 3')

        annotation1 = Annotation.objects.create(image=self.image, category=category1)
        annotation2 = Annotation.objects.create(image=self.image2, category=category2)
        annotation3 = Annotation.objects.create(image=self.image3, category=category3)

        annotation_boundingbox1 = Annotation.objects.create(image=self.image, category=category1, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        annotation_boundingbox2 = Annotation.objects.create(image=self.image2, category=category2, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        annotation_boundingbox2 = Annotation.objects.create(image=self.image3, category=category3, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)

        annotation_segmentation1 = Annotation.objects.create(image=self.image, category=category1, segmentation=[[10,10,10,20,20,20,20,10]])
        annotation_segmentation2 = Annotation.objects.create(image=self.image2, category=category2, segmentation=[[10,10,10,20,20,20,20,10]])
        annotation_segmentation2 = Annotation.objects.create(image=self.image3, category=category3, segmentation=[[10,10,10,20,20,20,20,10]])


        query_string = urlencode({ 'filter' : {'annotation': category1.id} })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.image.id])


        query_string = urlencode({ 'filter' : {'boundingbox': category2.id} })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.image2.id])


        query_string = urlencode({ 'filter' : {'segmentation': category3.id} })
        response = self.client.get('/api/images/?' + query_string)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['id'] for e in response.data], [self.image3.id])


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
            'url': self.image_url,
            'dataset': self.dataset.id
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], self.image_name)


    def test_show(self):
        response = self.client.get('/api/images/' + str(self.image.id) + '/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.image_name)


    def test_edit(self):
        response1 = self.client.post('/api/images/', { 'name': 'old_name', 'url': 'http://test.com/image.jpg', 'dataset': self.dataset.id })
        created_id = response1.data['id']
        self.assertEqual(response1.status_code, 201)

        new_data = { 'name': 'new_name', 'url': 'http://test.com/new_image.jpg', 'dataset': self.dataset.id }
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
