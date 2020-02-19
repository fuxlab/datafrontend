from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode
import io, zipfile, csv, json

from projects.models import Project
from images.models import Image
from datasets.models import Dataset
from categories.models import Category

from images.export import ImageExport

from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation


class TestImagesExportApi(TestCase):


    def setUp(self):
        self.client = Client()
        self.base_url = '/api/images/export/'

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


    def createAnnotations(self):
        self.annotation_segmentation1 = AnnotationSegmentation.objects.create(image=self.image, category=self.category, mask='segmentation_mask1')
        self.annotation_segmentation2 = AnnotationSegmentation.objects.create(image=self.image, category=self.category2, mask='segmentation_mask2')
        self.annotation_segmentation3 = AnnotationSegmentation.objects.create(image=self.image, category=self.category3, mask='segmentation_mask3')

        self.annotation_boundingbox1 = AnnotationBoundingbox.objects.create(image=self.image, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        self.annotation2 = Annotation.objects.create(image=self.image2, category=self.category2)

    
    def test_images_export_segmentation_with_single_category_filter_zip_in_coco_format(self):
        self.createAnnotations()

        url = '/api/images/export.zip'
        query_string = urlencode({ 'filter' : {
            'category': [self.category.id],
            'type': 'segmentation',
            'format': 'coco'
        }})
        response = self.client.get(url + '?' + query_string)            

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        
        downloaded_zip = zipfile.ZipFile(io.BytesIO(response.content))
        
        self.assertEqual(['a.json'], downloaded_zip.namelist())
        
        data = {}
        for file_name in downloaded_zip.namelist():
            file_a = downloaded_zip.open(file_name)
            data = json.load(io.TextIOWrapper(file_a))

        print(data['annotations'], [
          {'id': 31, 'image_id': 73, 'category_id': 95, 'area': 0, 'iscrowd': 0, 'segmentation': 'segmentation_mask1'},
          {'id': 31, 'image_id': 73, 'category_id': 95, 'area': 0, 'iscrowd': 0, 'segmentation': 'segmentation_mask2'},
          {'id': 31, 'image_id': 73, 'category_id': 95, 'area': 0, 'iscrowd': 0, 'segmentation': 'segmentation_mask3'}
        ])
        #self.assertEqual(len(data['images']), 2) # images
        #self.assertEqual([c['name'] for c in data['categories']], [self.category.name, self.category2.name]) # images
        