from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from categories.models import Category
from projects.models import Project

from datasets.models import Dataset
from images.models import Image
from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation


class TestModelCategories(TestCase):


    def setUp(self):
        self.client = Client()
        self.category_name = 'Categoryname'
        self.project = Project.objects.create(name='Testproject 1')
        self.dataset = Dataset.objects.create(name='test', project=self.project)
        self.category = Category.objects.create(name=self.category_name, project=self.project)
        self.category2 = Category.objects.create(name=self.category_name + ' 2', project=self.project)


    def test_counts(self):

        image = Image.objects.create(url='123456', dataset=self.dataset)

        Annotation.objects.create(category=self.category, image=image)
        Annotation.objects.create(category=self.category2, image=image)

        AnnotationBoundingbox.objects.create(category=self.category, image=image)
        AnnotationBoundingbox.objects.create(category=self.category2, image=image)

        AnnotationSegmentation.objects.create(category=self.category, image=image)
        AnnotationSegmentation.objects.create(category=self.category2, image=image)

        self.assertEqual(self.category.images_count(), 1)
        self.assertEqual(self.category.annotations_count(), 1)
        self.assertEqual(self.category.segmentations_count(), 1)
