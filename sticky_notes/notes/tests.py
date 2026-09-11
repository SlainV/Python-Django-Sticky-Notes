from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    def setUp(self):
        Note.objects.create(title="Test Title", content="This is a test note.",
                            color="#FF0000")

    def test_note_creation(self):
        note = Note.objects.get(id=1)
        self.assertEqual(note.title, "Test Title")

    def test_note_content(self):
        note = Note.objects.get(id=1)
        self.assertEqual(note.content, "This is a test note.")

    def test_note_color(self):
        note = Note.objects.get(id=1)
        self.assertEqual(note.color, "#FF0000")


class NotesViewTest(TestCase):
    def setUp(self):
        Note.objects.create(title="Test Title", content="This is a test note.",
                            color="#FF000")

    def test_notes_list_view(self):
        response = self.client.get(reverse('list_notes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/list.html')
        self.assertContains(response, "Test Title")
