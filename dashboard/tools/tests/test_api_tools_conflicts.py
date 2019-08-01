import json

from django.test import TestCase
from django.test import Client

from rest_framework.test import APIRequestFactory
from background_task.models import Task

from projects.models import Project
from categories.models import Category
from datasets.models import Dataset
from images.models import Image
from tools.models import Conflict


class TestApiToolsConflicts(TestCase):


    def setUp(self):
        self.client = Client()
        self.base_path = '/api/conflicts/'
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test 1', project=self.project)
        self.category = Category.objects.create(name='Test Category 1', project=self.project)
        self.image = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)

        self.init_conflict = Conflict.objects.create(
            reason=Conflict.REASON_AN_BB_DUP,
            affected_ids=[1,2],
            message=('some message')
        )


    def test_index(self):
        response = self.client.get(self.base_path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.init_conflict.id)
