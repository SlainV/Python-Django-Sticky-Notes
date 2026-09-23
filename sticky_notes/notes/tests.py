from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import NoteForm
from .models import Note


class NoteModelTest(TestCase):
    """Tests for the Note model."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Test Title",
            content="This is a test note.",
            color="#FF0000",
        )

    def test_note_creation(self):
        """A note should be created with the supplied title."""
        self.assertEqual(self.note.title, "Test Title")

    def test_note_content(self):
        """A note should store its content."""
        self.assertEqual(
            self.note.content,
            "This is a test note.",
        )

    def test_note_color(self):
        """A note should store its selected colour."""
        self.assertEqual(self.note.color, "#FF0000")

    def test_default_color(self):
        """A note should use the default colour when none is supplied."""
        note = Note.objects.create(
            title="Default Colour",
            content="This note uses the default colour.",
        )

        self.assertEqual(note.color, "#d2691e")

    def test_created_at_is_automatically_set(self):
        """A creation date should be added automatically."""
        self.assertIsNotNone(self.note.created_at)

    def test_empty_title_fails_model_validation(self):
        """An empty title should not pass model validation."""
        note = Note(
            title="",
            content="Content without a title.",
            color="#00FF00",
        )

        with self.assertRaises(ValidationError):
            note.full_clean()

    def test_title_longer_than_maximum_fails_validation(self):
        """A title longer than 100 characters should be invalid."""
        note = Note(
            title="A" * 101,
            content="Test content.",
            color="#00FF00",
        )

        with self.assertRaises(ValidationError):
            note.full_clean()

    def test_invalid_color_fails_model_validation(self):
        """A non-hexadecimal colour should fail model validation."""
        note = Note(
            title="Invalid Colour",
            content="This note has an invalid colour.",
            color="invalid",
        )

        with self.assertRaises(ValidationError):
            note.full_clean()

    def test_incomplete_hex_color_fails_model_validation(self):
        """A hexadecimal colour containing too few digits should be invalid."""
        note = Note(
            title="Incomplete Colour",
            content="This colour has only five digits.",
            color="#FF000",
        )

        with self.assertRaises(ValidationError):
            note.full_clean()


class NoteFormTest(TestCase):
    """Tests for the NoteForm."""

    def test_form_accepts_valid_data(self):
        """The form should accept valid note information."""
        form = NoteForm(
            data={
                "title": "Shopping List",
                "content": "Buy milk and bread.",
                "color": "#FFFF00",
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_saves_valid_note(self):
        """A valid form should create a note."""
        form = NoteForm(
            data={
                "title": "Shopping List",
                "content": "Buy milk and bread.",
                "color": "#FFFF00",
            }
        )

        self.assertTrue(form.is_valid())

        note = form.save()

        self.assertIsNotNone(note.pk)
        self.assertEqual(note.title, "Shopping List")
        self.assertEqual(note.content, "Buy milk and bread.")
        self.assertEqual(note.color, "#FFFF00")

    def test_form_rejects_empty_title(self):
        """The title field should be required."""
        form = NoteForm(
            data={
                "title": "",
                "content": "Content without a title.",
                "color": "#FF0000",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_rejects_missing_title(self):
        """The form should be invalid when the title is omitted."""
        form = NoteForm(
            data={
                "content": "Content without a title.",
                "color": "#FF0000",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_rejects_title_longer_than_100_characters(self):
        """The form should reject titles exceeding the model limit."""
        form = NoteForm(
            data={
                "title": "A" * 101,
                "content": "Test content.",
                "color": "#FF0000",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_rejects_invalid_color(self):
        """The form should reject a non-hexadecimal colour."""
        form = NoteForm(
            data={
                "title": "Invalid Colour",
                "content": "This note has an invalid colour.",
                "color": "invalid",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("color", form.errors)

    def test_form_rejects_incomplete_hex_color(self):
        """The form should reject a colour with fewer than six hex digits."""
        form = NoteForm(
            data={
                "title": "Incomplete Colour",
                "content": "This note has an incomplete colour.",
                "color": "#FF000",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("color", form.errors)

    def test_form_rejects_empty_content(self):
        """The content field should be required."""
        form = NoteForm(
            data={
                "title": "Empty Note",
                "content": "",
                "color": "#FF0000",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)


class NotesListViewTest(TestCase):
    """Tests for the note list view."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Test Title",
            content="This is a test note.",
            color="#FF0000",
        )

    def test_notes_list_view_returns_success(self):
        """The list page should load successfully."""
        response = self.client.get(reverse("list_notes"))

        self.assertEqual(response.status_code, 200)

    def test_notes_list_view_uses_correct_template(self):
        """The list page should use the notes list template."""
        response = self.client.get(reverse("list_notes"))

        self.assertTemplateUsed(response, "notes/list.html")

    def test_notes_list_view_displays_note(self):
        """Existing notes should appear on the list page."""
        response = self.client.get(reverse("list_notes"))

        self.assertContains(response, self.note.title)
        self.assertContains(response, self.note.content)

    def test_notes_list_view_context_contains_notes(self):
        """The view context should contain the notes queryset."""
        response = self.client.get(reverse("list_notes"))

        self.assertIn("notes", response.context)
        self.assertIn(self.note, response.context["notes"])

    def test_notes_list_view_has_page_title(self):
        """The view should supply the correct page title."""
        response = self.client.get(reverse("list_notes"))

        self.assertEqual(
            response.context["page_title"],
            "Sticky Notes",
        )

    def test_empty_notes_list_view(self):
        """The list page should still load when no notes exist."""
        Note.objects.all().delete()

        response = self.client.get(reverse("list_notes"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notes"].count(), 0)


class CreateNoteViewTest(TestCase):
    """Tests for creating notes."""

    def test_create_note_get_request(self):
        """A GET request should display an empty note form."""
        response = self.client.get(reverse("create_note"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/form.html")
        self.assertIsInstance(response.context["form"], NoteForm)

    def test_create_note_with_valid_post_data(self):
        """Valid POST data should create a note."""
        response = self.client.post(
            reverse("create_note"),
            data={
                "title": "Created Note",
                "content": "This note was created by a test.",
                "color": "#00FF00",
            },
        )

        self.assertEqual(Note.objects.count(), 1)

        note = Note.objects.get(title="Created Note")

        self.assertIsNotNone(note.pk)
        self.assertEqual(
            note.content,
            "This note was created by a test.",
        )
        self.assertEqual(note.color, "#00FF00")

        self.assertRedirects(
            response,
            reverse("list_notes"),
        )

    def test_create_note_with_empty_title(self):
        """An empty title should redisplay the form without creating a note."""
        response = self.client.post(
            reverse("create_note"),
            data={
                "title": "",
                "content": "Content without a title.",
                "color": "#00FF00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 0)
        self.assertTemplateUsed(response, "notes/form.html")
        self.assertIn("title", response.context["form"].errors)

    def test_create_note_with_invalid_color(self):
        """An invalid colour should not create a note."""
        response = self.client.post(
            reverse("create_note"),
            data={
                "title": "Invalid Colour",
                "content": "This should not be saved.",
                "color": "invalid",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 0)
        self.assertIn("color", response.context["form"].errors)


class EditNoteViewTest(TestCase):
    """Tests for editing notes."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Original Title",
            content="Original content.",
            color="#FF0000",
        )

    def test_edit_note_get_request(self):
        """A GET request should display a form containing the note."""
        response = self.client.get(
            reverse("edit_note", args=[self.note.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/form.html")
        self.assertEqual(
            response.context["form"].instance,
            self.note,
        )

    def test_edit_note_with_valid_post_data(self):
        """Valid POST data should update the existing note."""
        original_pk = self.note.pk

        response = self.client.post(
            reverse("edit_note", args=[self.note.pk]),
            data={
                "title": "Updated Title",
                "content": "Updated content.",
                "color": "#0000FF",
            },
        )

        self.note.refresh_from_db()

        self.assertEqual(self.note.pk, original_pk)
        self.assertEqual(self.note.title, "Updated Title")
        self.assertEqual(self.note.content, "Updated content.")
        self.assertEqual(self.note.color, "#0000FF")
        self.assertEqual(Note.objects.count(), 1)

        self.assertRedirects(
            response,
            reverse("list_notes"),
        )

    def test_edit_note_with_empty_title(self):
        """Invalid edit data should not update the note."""
        response = self.client.post(
            reverse("edit_note", args=[self.note.pk]),
            data={
                "title": "",
                "content": "Changed content.",
                "color": "#0000FF",
            },
        )

        self.note.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.note.title, "Original Title")
        self.assertEqual(self.note.content, "Original content.")
        self.assertIn("title", response.context["form"].errors)

    def test_edit_note_with_invalid_color(self):
        """An invalid colour should not update the note."""
        response = self.client.post(
            reverse("edit_note", args=[self.note.pk]),
            data={
                "title": "Changed Title",
                "content": "Changed content.",
                "color": "invalid",
            },
        )

        self.note.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.note.title, "Original Title")
        self.assertEqual(self.note.color, "#FF0000")
        self.assertIn("color", response.context["form"].errors)

    def test_edit_missing_note_returns_404(self):
        """Editing a nonexistent note should return a 404 response."""
        response = self.client.get(
            reverse("edit_note", args=[99999])
        )

        self.assertEqual(response.status_code, 404)


class DeleteNoteViewTest(TestCase):
    """Tests for deleting notes."""

    def setUp(self):
        self.note = Note.objects.create(
            title="Delete Me",
            content="This note will be deleted.",
            color="#FF0000",
        )

    def test_delete_note_with_post_request(self):
        """A POST request should delete the selected note."""
        note_pk = self.note.pk

        response = self.client.post(
            reverse("delete_note", args=[note_pk])
        )

        self.assertFalse(
            Note.objects.filter(pk=note_pk).exists()
        )
        self.assertRedirects(
            response,
            reverse("list_notes"),
        )

    def test_delete_note_get_request_does_not_delete_note(self):
        """A GET request should not delete a note."""
        note_pk = self.note.pk

        response = self.client.get(
            reverse("delete_note", args=[note_pk])
        )

        self.assertTrue(
            Note.objects.filter(pk=note_pk).exists()
        )
        self.assertRedirects(
            response,
            reverse("list_notes"),
        )

    def test_delete_missing_note_with_post_returns_404(self):
        """Deleting a nonexistent note by POST should return 404."""
        response = self.client.post(
            reverse("delete_note", args=[99999])
        )

        self.assertEqual(response.status_code, 404)
