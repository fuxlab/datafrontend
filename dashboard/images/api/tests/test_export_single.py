from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart

from django.contrib.admin.utils import flatten

from urllib.parse import urlencode
import io, zipfile, csv, json

from projects.models import Project
from images.models import Image
from datasets.models import Dataset
from categories.models import Category

from images.api import ImageExport

from annotations.models import Annotation


class TestImagesApiExportSingle(TestCase):


    def setUp(self):
        self.client = Client()
        self.base_url = '/api/images/export/download'

        self.image_base_name = 'Testimage'
        self.image_base_url = 'http://test.com/image'

        self.project = Project.objects.create(name='Project 1')
        
        self.dataset = Dataset.objects.create(name='Test Dataset 1', project=self.project)
        self.category = Category.objects.create(name='Categoryname 1', project=self.project)
        self.image = Image.objects.create(name=self.image_base_name + '1', url=self.image_base_url + '1', dataset=self.dataset, width=100, height=200)

        self.dataset2 = Dataset.objects.create(name='Test Dataset 2', project=self.project)
        self.category2 = Category.objects.create(name='Categoryname 2', project=self.project)
        self.image2 = Image.objects.create(name=self.image_base_name + '2', url=self.image_base_url + '2', dataset=self.dataset2, width=100, height=200)

        self.dataset3 = Dataset.objects.create(name='Test Dataset 3', project=self.project)
        self.category3 = Category.objects.create(name='Categoryname 3', project=self.project)
        self.image3 = Image.objects.create(name=self.image_base_name + '3', url=self.image_base_url + '3', dataset=self.dataset3, width=100, height=200)

        self.annotation_boundingbox1 = Annotation.objects.create(image=self.image, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        self.annotation_boundingbox2 = Annotation.objects.create(image=self.image2, category=self.category2, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)

        self.annotation_segmentation1 = Annotation.objects.create(image=self.image, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])
        self.annotation_segmentation2 = Annotation.objects.create(image=self.image3, category=self.category3, segmentation=[[10,10,10,20,20,20,20,10]])

        self.annotation2 = Annotation.objects.create(image=self.image2, category=self.category2)
        self.annotation3 = Annotation.objects.create(image=self.image3, category=self.category3)


    def test_export_without_filter(self):
        response = self.client.get(self.base_url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data['images']), 0)
        self.assertEqual(len(response_data['annotations']), 0)
        self.assertEqual(len(response_data['categories']), 0)


    def test_export_without_type(self):
        query_string = urlencode({ 'filter' : {
            'dataset': [self.dataset.id, self.dataset2.id],
        }})
        response = self.client.get(self.base_url + '?' + query_string)
        response_data = json.loads(response.content)

        all_keys = list(set(flatten([list(annotation.keys()) for annotation in response_data['annotations']])))
        all_keys.sort()
        self.assertEqual(all_keys, ['area', 'bbox', 'category_id', 'id', 'image_id', 'iscrowd', 'mask', 'segmentation'])

        exported_annotation_ids = [ annotation['id'] for annotation in response_data['annotations'] ]
        expected_annotation_ids = [self.annotation_boundingbox1.id, self.annotation_boundingbox2.id, self.annotation_segmentation1.id, self.annotation2.id]
        self.assertEqual(exported_annotation_ids, expected_annotation_ids)

    
    def test_export_without_annotation_type_filter(self):
        query_string = urlencode({ 'filter' : {
            'dataset': [self.dataset.id, self.dataset2.id],
            'type': 'annotation'
        }})
        response = self.client.get(self.base_url + '?' + query_string)
        response_data = json.loads(response.content)

        all_keys = list(set(flatten([list(annotation.keys()) for annotation in response_data['annotations']])))
        all_keys.sort()
        self.assertEqual(all_keys, ['category_id', 'id', 'image_id'])

        exported_annotation_ids = [ annotation['id'] for annotation in response_data['annotations'] ]
        expected_annotation_ids = [self.annotation_boundingbox1.id, self.annotation_boundingbox2.id, self.annotation_segmentation1.id, self.annotation2.id]
        self.assertEqual(exported_annotation_ids, expected_annotation_ids)


    def test_export_with_boundingbox_type_filter(self):
        query_string = urlencode({ 'filter' : {
            'category': [self.category.id],
            'type': 'boundingbox'
        }})
        response = self.client.get(self.base_url + '?' + query_string)
        response_data = json.loads(response.content)

        all_keys = list(set(flatten([list(annotation.keys()) for annotation in response_data['annotations']])))
        all_keys.sort()
        self.assertEqual(all_keys, ['area', 'bbox', 'category_id', 'id', 'image_id', 'iscrowd'])

        exported_annotation_ids = [ annotation['id'] for annotation in response_data['annotations'] ]
        expected_annotation_ids = [self.annotation_boundingbox1.id, self.annotation_segmentation1.id]
        self.assertEqual(exported_annotation_ids, expected_annotation_ids)


    def test_export_with_segmentation_type_filter(self):
        query_string = urlencode({ 'filter' : {
            'category': [self.category.id],
            'type': 'segmentation'
        }})
        response = self.client.get(self.base_url + '?' + query_string)
        response_data = json.loads(response.content)

        all_keys = list(set(flatten([list(annotation.keys()) for annotation in response_data['annotations']])))
        all_keys.sort()
        self.assertEqual(all_keys, ['area', 'bbox', 'category_id', 'id', 'image_id', 'iscrowd', 'mask', 'segmentation'])

        exported_annotation_ids = [ annotation['id'] for annotation in response_data['annotations'] ]
        expected_annotation_ids = [self.annotation_segmentation1.id]
        self.assertEqual(exported_annotation_ids, expected_annotation_ids)
