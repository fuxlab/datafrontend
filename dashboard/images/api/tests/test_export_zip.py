from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode
import io, zipfile, csv, json

from projects.models import Project
from images.models import Image
from datasets.models import Dataset
from categories.models import Category

from images.api import ImageExport

from annotations.models import Annotation


class TestImagesExportApi(TestCase):


    def setUp(self):
        self.client = Client()
        self.base_url = '/api/images/export/download'

        self.image_base_name = 'Testimage'
        self.image_base_url = 'http://test.com/image'

        self.project = Project.objects.create(name='Project 1')
        
        self.dataset = Dataset.objects.create(name='Test Dataset 1', project=self.project)
        self.category = Category.objects.create(name='Categoryname 1', project=self.project)
        self.image = Image.objects.create(name=self.image_base_name + '1', url=self.image_base_url + '1', dataset=self.dataset, width=100, height=200)

        self.annotation2 = Annotation.objects.create(image=self.image, category=self.category)

        self.annotation_segmentation1 = Annotation.objects.create(image=self.image, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])
        self.annotation_segmentation2 = Annotation.objects.create(image=self.image, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])
        self.annotation_segmentation3 = Annotation.objects.create(image=self.image, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])

        self.annotation_boundingbox1 = Annotation.objects.create(image=self.image, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)

            
    def test_images_export_segmentation_with_single_category_filter_zip_in_coco_format(self):
        query_string = urlencode({ 'filter' : {
            'category': [self.category.id],
            'type': 'segmentation',
            'format': 'coco',
            'split': '80_20'
        }})
        response = self.client.get(self.base_url + '?' + query_string)            

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        
        downloaded_zip = zipfile.ZipFile(io.BytesIO(response.content))
        
        self.assertEqual(['a.json', 'b.json'], downloaded_zip.namelist())
        
        data = {}
        for file_name in downloaded_zip.namelist():
            file_a = downloaded_zip.open(file_name)
            data[file_name] = json.load(io.TextIOWrapper(file_a))

        self.assertEqual(len(data['a.json']['annotations']), 2)
        self.assertEqual(len(data['b.json']['annotations']), 1)

        self.assertEqual(len(data['a.json']['images']), 1)
        self.assertEqual(len(data['a.json']['images']), 1)

