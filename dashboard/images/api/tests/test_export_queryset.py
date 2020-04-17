from django.test import TestCase

from projects.models import Project
from images.models import Image
from datasets.models import Dataset
from categories.models import Category

from images.api import ImageExport

from annotations.models import Annotation

class TestImagesApiExportQueryset(TestCase):


    def setUp(self):
        self.base_url = '/api/images/export/download'

        self.project = Project.objects.create(name='Project 1')
        self.dataset1 = Dataset.objects.create(name='Test Dataset 1', project=self.project)
        self.dataset2 = Dataset.objects.create(name='Test Dataset 2', project=self.project)
        self.dataset3 = Dataset.objects.create(name='Test Dataset 3', project=self.project)
        
        self.category1 = Category.objects.create(name='Category 1', project=self.project)
        self.category2 = Category.objects.create(name='Category 2', project=self.project)
        self.category3 = Category.objects.create(name='Category 3', project=self.project)
        
        self.image1 = Image.objects.create(name='Text Image 1', url='http://url.1', dataset=self.dataset1)
        self.image2 = Image.objects.create(name='Text Image 2', url='http://url.2', dataset=self.dataset2)
        self.image3 = Image.objects.create(name='Text Image 3', url='http://url.3', dataset=self.dataset3)

        self.annotation1 = Annotation.objects.create(image=self.image1, category=self.category1)
        self.annotation2 = Annotation.objects.create(image=self.image2, category=self.category2)
        self.annotation3 = Annotation.objects.create(image=self.image3, category=self.category3)

        self.annotation_boundingbox1 = Annotation.objects.create(image=self.image1, category=self.category1, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        self.annotation_boundingbox2 = Annotation.objects.create(image=self.image2, category=self.category2, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        self.annotation_boundingbox3 = Annotation.objects.create(image=self.image3, category=self.category3, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)

        self.annotation_segmentation1 = Annotation.objects.create(image=self.image1, category=self.category1, segmentation=[[10,10,10,20,20,20,20,10]])
        self.annotation_segmentation2 = Annotation.objects.create(image=self.image2, category=self.category2, segmentation=[[10,10,10,20,20,20,20,10]])
        self.annotation_segmentation3 = Annotation.objects.create(image=self.image3, category=self.category3, segmentation=[[10,10,10,20,20,20,20,10]])


    def test_queryset_with_dataset_filter(self):
        export_params = {
            'dataset': [ self.dataset1.id, self.dataset2.id ]
        }

        view_obj = ImageExport()
        results = view_obj.queryset(export_params)
        self.assertEqual([
            self.annotation1.id,
            self.annotation2.id,
            self.annotation_boundingbox1.id,
            self.annotation_boundingbox2.id,
            self.annotation_segmentation1.id,
            self.annotation_segmentation2.id ], [result.id for result in results])


    def test_queryset_with_category_filter(self):
        export_params = {
            'category': [ self.category1.id, self.category2.id ],
        }

        view_obj = ImageExport()
        results = view_obj.queryset(export_params)
        self.assertEqual([  self.annotation1.id,
            self.annotation2.id,
            self.annotation_boundingbox1.id,
            self.annotation_boundingbox2.id,
            self.annotation_segmentation1.id,
            self.annotation_segmentation2.id ], [result.id for result in results])


    def test_queryset_boundingbox_filter(self):
        export_params = {
            'category':[ self.category1.id ],
            'type': 'boundingbox',
        }

        view_obj = ImageExport()
        results = view_obj.queryset(export_params)
        self.assertEqual([result.id for result in results], [ self.annotation_boundingbox1.id, self.annotation_segmentation1.id ])


    def test_queryset_segmentation_filter(self):
        export_params = {
            'category':[ self.category1.id ],
            'type': 'segmentation',
        }

        view_obj = ImageExport()
        results = view_obj.queryset(export_params)
        self.assertEqual([result.id for result in results], [ self.annotation_segmentation1.id ])

