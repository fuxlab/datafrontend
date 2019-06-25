from django.test import TestCase
from django.test import Client
from django.test.client import encode_multipart
from urllib.parse import urlencode

from categories.models import Category
from projects.models import Project

from datasets.models import Dataset
from images.models import Image
from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation


class TestModelDatasets(TestCase):


    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(name='Testproject 1')


    def test_counts(self):
        dataset = Dataset.objects.create(name='test', project=self.project)
        dataset2 = Dataset.objects.create(name='test2', project=self.project)

        image = Image.objects.create(url='123456', dataset=dataset)
        image = Image.objects.create(url='123456', dataset=dataset2)

        self.assertEqual(dataset.images_count(), 1)
