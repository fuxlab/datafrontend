from django.test import TestCase
from django.test import Client

from notes.models import Note

class TestNotes(TestCase):

  def setUp(self):
    self.note_text = 'First Note!'
    self.note = Note.objects.create(text=self.note_text)

  def test_index(self):
    c = Client()
    response = c.get('/api/notes/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data[0]['text'], self.note_text)

  def test_creation(self):
    c = Client()
    response = c.post('/api/notes/', { 'text': self.note_text })

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['text'], self.note_text)
  
  def test_show(self):
    c = Client()
    response = c.get('/api/notes/' + str(self.note.id) + '/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['text'], self.note_text)

  def test_delete(self):
    c = Client()
    response = c.delete('/api/notes/' + str(self.note.id) + '/')
    self.assertEqual(response.status_code, 204)
