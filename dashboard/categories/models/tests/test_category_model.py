from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from categories.models import Category
from projects.models import Project

from datasets.models import Dataset
from images.models import Image
from annotations.models import Annotation, Annotation, Annotation


class TestCategoryModel(TestCase):


    def setUp(self):
        self.client = Client()
        self.category_name = 'Categoryname'
        self.project = Project.objects.create(name='Testproject 1')
        self.project2 = Project.objects.create(name='Testproject 2')
        
        self.dataset = Dataset.objects.create(name='test', project=self.project)
        self.dataset2 = Dataset.objects.create(name='test 2', project=self.project2)
        
        self.category = Category.objects.create(name=self.category_name, project=self.project)
        self.category2 = Category.objects.create(name=self.category_name + ' 2', project=self.project)


    def test_counts(self):

        image = Image.objects.create(url='123456', dataset=self.dataset)
        image2 = Image.objects.create(url='1234562', dataset=self.dataset2)

        Annotation.objects.create(category=self.category, image=image)
        Annotation.objects.create(category=self.category2, image=image2)

        Annotation.objects.create(category=self.category, image=image, x_min=10, y_min=10, x_max=20, y_max=20)
        Annotation.objects.create(category=self.category2, image=image2, x_min=10, y_min=10, x_max=20, y_max=20)

        Annotation.objects.create(category=self.category, image=image, segmentation=[[10,10,10,20,20,20,20,10]])
        Annotation.objects.create(category=self.category2, image=image2, segmentation=[[10,10,10,20,20,20,20,10]])

        self.assertEqual(self.category.images_count(), 1)
        self.assertEqual(self.category.annotations_count(), 3)
        self.assertEqual(self.category.boundingboxes_count(), 2)
        self.assertEqual(self.category.segmentations_count(), 1)
