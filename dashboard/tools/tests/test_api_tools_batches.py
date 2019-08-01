import json

from django.test import TestCase
from django.test import Client

from rest_framework.test import APIRequestFactory
from background_task.models import Task

from projects.models import Project
from categories.models import Category
from datasets.models import Dataset
from images.models import Image
from tools.models import Batch


class TestApiToolsBatches(TestCase):


    def setUp(self):
        self.client = Client()
        self.base_path = '/api/batches/'
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test 1', project=self.project)
        self.category = Category.objects.create(name='Test Category 1', project=self.project)
        self.image = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)
        
        self.init_batch = Batch.objects.create(params={'key': 'value'}, log=['elem1', 'elem2'])


    def test_index(self):
        response = self.client.get(self.base_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.init_batch.id)


    def test_change_image_datasets(self):
        response = self.client.post(self.base_path, data=json.dumps({
            'action'    : 'update_images_dataset',
            'params'    : [[1,2,3,4], 1]
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.all()[0].task_name, 'tools.tasks.batches.update_images_dataset')
        self.assertEqual(Task.objects.all()[0].params()[0][0], response.data['id'])
        

    def test_change_annotations_categories(self):
        response = self.client.post(self.base_path, data=json.dumps({
            'action'    : 'update_annotations_category',
            'params'    : [[1,2,3,4], 1]
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.all()[0].task_name, 'tools.tasks.batches.update_annotations_category')
        self.assertEqual(Task.objects.all()[0].params()[0][0], response.data['id'])


    def test_change_annotation_boundingboxes(self):
        response = self.client.post(self.base_path, data=json.dumps({
            'action'    : 'update_annotation_boundingboxes_category',
            'params'    : [[1,2,3,4], 1]
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.all()[0].task_name, 'tools.tasks.batches.update_annotation_boundingboxes_category')
        self.assertEqual(Task.objects.all()[0].params()[0][0], response.data['id'])


    def test_change_annotations_sementations(self):
        response = self.client.post(self.base_path, data=json.dumps({
            'action'    : 'update_annotation_segmentations_category',
            'params'    : [[1,2,3,4], 1]
        }), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.all()[0].task_name, 'tools.tasks.batches.update_annotation_segmentations_category')
        self.assertEqual(Task.objects.all()[0].params()[0][0], response.data['id'])

