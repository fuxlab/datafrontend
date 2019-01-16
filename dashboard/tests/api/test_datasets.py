from django.test import TestCase
from django.test import Client

from datasets.models import Dataset

class TestProjects(TestCase):

  def setUp(self):
    self.dataset_name = 'Name'
    self.dataset_identifier = 'Identifier'
    self.project = Dataset.objects.create(name=self.dataset_name)

  def test_index(self):
    c = Client()
    response = c.get('/api/datasets/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data[0]['name'], self.dataset_name)

  def test_creation(self):
    c = Client()
    response = c.post('/api/datasets/', { 'name': self.dataset_name, 'identifier': self.dataset_identifier })

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['name'], self.dataset_name)
  
  def test_show(self):
    c = Client()
    response = c.get('/api/datasets/' + str(self.project.id) + '/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['name'], self.dataset_name)

  def test_delete(self):
    c = Client()
    response = c.delete('/api/datasets/' + str(self.project.id) + '/')
    self.assertEqual(response.status_code, 204)
