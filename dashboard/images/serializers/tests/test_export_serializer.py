from django.test import TestCase

from projects.models import Project
from datasets.models import Dataset
from categories.models import Category
from images.models import Image
from annotations.models import Annotation

from images.serializers.export import ExportSerializer

class TestExportSerializer(TestCase):


    def setUp(self):
        self.project = Project.objects.create(name='Project 1')
        
        self.dataset = Dataset.objects.create(name='Test Dataset 1', project=self.project)
        self.category = Category.objects.create(name='Categoryname 1', project=self.project)
        self.image = Image.objects.create(name='Testimage 1', url='http://test.com/image1.jpg', dataset=self.dataset, width=100, height=200)

        self.annotation = Annotation.objects.create(image=self.image, category=self.category)
        self.segmentation = Annotation.objects.create(image=self.image, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])
        self.boundingbox = Annotation.objects.create(image=self.image, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)


    def test_basic_serialization(self):
        export_params = {
            'dataset': [ self.dataset.id ]
        }

        serializer = ExportSerializer(self.annotation, export_params=export_params)
        self.assertEqual(serializer.data, {
            'id': self.annotation.id,
            'type': 'all',
            'annotation_image': '/api/image/%s.png' % (self.annotation.id),
            'image': self.image.image(),
            'source': self.dataset.name
        })


    def test_annotation_serialization(self):
        export_params = {
            'type': 'annotation',
            'category': [ self.category.id ]
        }
        
        serializer = ExportSerializer(self.annotation, export_params=export_params)
        self.assertEqual(serializer.data, {
            'id': self.annotation.id,
            'type': 'annotation',
            'annotation_image': '/api/image/%s.png' % (self.annotation.id),
            'image': self.image.image(),
            'source': self.category.name
        })

    
    def test_boundingbox_serialization(self):
        export_params = {
            'type': 'boundingbox',
            'category': [ self.category.id ]
        }

        serializer = ExportSerializer(self.boundingbox, export_params=export_params)
        self.assertEqual(serializer.data, {
            'id': self.boundingbox.id,
            'type': 'boundingbox',
            'annotation_image': '/api/image/boundingbox_%s.png' % (self.boundingbox.id),
            'image': self.image.image(),
            'source': self.category.name
        })


    def test_segmentation_serialization(self):
        export_params = {
            'type': 'segmentation',
            'category': [ self.category.id ]
        }
        
        serializer = ExportSerializer(self.segmentation, export_params=export_params)
        self.assertEqual(serializer.data, {
            'id': self.segmentation.id,
            'type': 'segmentation',
            'annotation_image': '/api/image/segmentation_%s.png' % (self.segmentation.id),
            'image': self.image.image(),
            'source': self.category.name
        })
