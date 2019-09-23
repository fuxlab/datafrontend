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


class TestImagesExportZip(TestCase):


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
        self.annotation_boundingbox1 = AnnotationBoundingbox.objects.create(image=self.image, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        self.annotation_boundingbox2 = AnnotationBoundingbox.objects.create(image=self.image2, category=self.category2, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)

        self.annotation_segmentation1 = AnnotationSegmentation.objects.create(image=self.image, category=self.category, mask='segmentation_mask')
        self.annotation_segmentation2 = AnnotationSegmentation.objects.create(image=self.image3, category=self.category3, mask='segmentation_mask')

        self.annotation2 = Annotation.objects.create(image=self.image2, category=self.category2)
        self.annotation3 = Annotation.objects.create(image=self.image3, category=self.category3)


    def test_images_export_zip(self):
        self.createAnnotations()

        url = '/api/images/export.zip'
        query_string = urlencode({ 'filter' : {
            'dataset': [self.dataset.id, self.dataset2.id],
            'type': 'all'
        } })
        response = self.client.get(url + '?' + query_string)            

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        
        downloaded_zip = zipfile.ZipFile(io.BytesIO(response.content))
        
        self.assertEqual(['a.csv'], downloaded_zip.namelist())
        
        content = []
        for file_name in downloaded_zip.namelist():
            file_a = downloaded_zip.open(file_name)
            content.append([ list(row) for row in csv.reader(io.TextIOWrapper(file_a)) ])
        
        self.assertEqual(len(content), 1)                             # files
        self.assertEqual(len(content[0]), 2)                          # images

        # we cannot be sure in which file the data is due to shuffeling
        result_data = [content[0][0][0], content[0][1][0]]
        self.assertTrue(('%s.png' % (self.image.id)) in result_data)        # image1
        self.assertTrue(('%s.png' % (self.image2.id)) in result_data)       # image2


    def test_images_export_coco_zip(self):
        self.createAnnotations()

        url = '/api/images/export.zip'
        query_string = urlencode({ 'filter' : {
            'dataset': [self.dataset.id, self.dataset2.id],
            'type': 'all',
            'format': 'coco'
        } })
        response = self.client.get(url + '?' + query_string)            

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        
        downloaded_zip = zipfile.ZipFile(io.BytesIO(response.content))
        
        self.assertEqual(['a.json'], downloaded_zip.namelist())
        
        data = {}
        for file_name in downloaded_zip.namelist():
            file_a = downloaded_zip.open(file_name)
            data = json.load(io.TextIOWrapper(file_a))

        self.assertEqual(len(data['images']), 2) # images
        self.assertEqual([c['name'] for c in data['categories']], [self.dataset.name, self.dataset2.name]) # images


    def test_images_export_boundingboxes_zip(self):
        self.createAnnotations()

        url = '/api/images/export.zip'
        query_string = urlencode({ 'filter' : {
            'category': [self.category.id, self.category2.id],
            'type': 'boundingbox'
        }})
        response = self.client.get(url + '?' + query_string)            

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        
        downloaded_zip = zipfile.ZipFile(io.BytesIO(response.content))
        
        self.assertEqual(['a.csv'], downloaded_zip.namelist())
        
        content = []
        for file_name in downloaded_zip.namelist():
            file_a = downloaded_zip.open(file_name)
            content.append([ list(row) for row in csv.reader(io.TextIOWrapper(file_a)) ])

        self.assertEqual(len(content), 1)                             # files
        self.assertEqual(len(content[0]), 2)                          # images
        
        # we cannot be sure where data is due to shuffeling
        result_data = [content[0][0][0], content[0][1][0]]
        self.assertTrue(('boundingbox_%s.png' % (self.annotation_boundingbox1.id)) in result_data)        # image1
        self.assertTrue(('boundingbox_%s.png' % (self.annotation_boundingbox2.id)) in result_data)       # image2


    def test_images_export_coco_boundingboxes_zip(self):
        self.createAnnotations()

        url = '/api/images/export.zip'
        query_string = urlencode({ 'filter' : {
            'category': [self.category.id, self.category2.id],
            'type': 'boundingbox',
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

        self.assertEqual(len(data['images']), 2) # images
        self.assertEqual([c['name'] for c in data['categories']], [self.category.name, self.category2.name]) # images
        
        # we cannot be sure where data is due to shuffeling
        #result_data = [content[0][0][1], content[0][1][1]]
        #self.assertTrue(('/api/image/boundingbox_crop/%s.png' % (self.annotation_boundingbox1.id)) in result_data)        # image1
        #self.assertTrue(('/api/image/boundingbox_crop/%s.png' % (self.annotation_boundingbox2.id)) in result_data)       # image2


    def test_images_export_zip_with_split(self):
        self.createAnnotations()

        url = '/api/images/export.zip'
        query_string = urlencode({ 'filter' : {'dataset': [self.dataset.id, self.dataset2.id], 'split': '50_50'} })
        response = self.client.get(url + '?' + query_string)            

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        
        downloaded_zip = zipfile.ZipFile(io.BytesIO(response.content))
        
        self.assertEqual(['a.csv', 'b.csv'], downloaded_zip.namelist())
        
        content = []
        for file_name in downloaded_zip.namelist():
            file_a = downloaded_zip.open(file_name)
            content.append([ list(row) for row in csv.reader(io.TextIOWrapper(file_a)) ])
        
        self.assertEqual(len(content), 2)                             # files
        self.assertEqual(len(content[0]), 1)                          # file 1, images
        self.assertEqual(len(content[1]), 1)                          # file 2, images

        # we cannot be sure in which file the data is due to shuffeling
        result_data = [content[0][0][0], content[1][0][0]]
        self.assertTrue(('%s.png' % (self.image.id)) in result_data)        # image1
        self.assertTrue(('%s.png' % (self.image2.id)) in result_data)       # image2
