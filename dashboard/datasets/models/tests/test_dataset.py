from django.test import TestCase

from projects.models import Project

from datasets.models import Dataset
from images.models import Image


class TestModelsDataset(TestCase):


    def setUp(self):
        self.project = Project.objects.create(name='Testproject 1')


    def test_counts(self):
        dataset = Dataset.objects.create(name='test', project=self.project)
        dataset2 = Dataset.objects.create(name='test2', project=self.project)

        image = Image.objects.create(url='123456', dataset=dataset)
        image = Image.objects.create(url='123456', dataset=dataset2)

        self.assertEqual(dataset.images_count(), 1)

    
    def test_auto_set_identifier(self):
        dataset = Dataset.objects.create(name='This is a very strange name !"§', project=self.project)
        
        saved_dataset = Dataset.objects.get(id=dataset.id)
        self.assertEqual(saved_dataset.identifier, 'this-is-a-very-strange-name')


    def test_write_identifier(self):
        dataset = Dataset.objects.create(name='Name', identifier='new_name', project=self.project)
        
        saved_dataset = Dataset.objects.get(id=dataset.id)
        self.assertEqual(saved_dataset.identifier, 'new_name')


    def test_rewrite_identifier(self):
        dataset = Dataset.objects.create(name='Name', identifier='this $%/& is a stupid identifier', project=self.project)
        
        saved_dataset = Dataset.objects.get(id=dataset.id)
        self.assertEqual(saved_dataset.identifier, 'this-is-a-stupid-identifier')
