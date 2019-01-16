from django.test import TestCase
from django.test import Client

from projects.models import Project

class TestProjects(TestCase):

  def setUp(self):
    self.project_name = 'Testproject'
    self.project = Project.objects.create(name=self.project_name)

  def test_index(self):
    c = Client()
    response = c.get('/api/projects/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data[0]['name'], self.project_name)

  def test_creation(self):
    c = Client()
    response = c.post('/api/projects/', { 'name': self.project_name })

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['name'], self.project_name)
  
  def test_show(self):
    c = Client()
    response = c.get('/api/projects/' + str(self.project.id) + '/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['name'], self.project_name)

  def test_delete(self):
    c = Client()
    response = c.delete('/api/projects/' + str(self.project.id) + '/')
    self.assertEqual(response.status_code, 204)
