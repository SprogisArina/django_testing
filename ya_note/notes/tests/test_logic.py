from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.fixtures import (
    Base, ADD_URL, DELETE_URL, EDIT_URL, LOGIN_URL, SLUG, SUCCESS_URL, TEXT,
    TITLE
)


class TestNoteCreation(Base):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': TITLE,
            'text': TEXT,
            'slug': SLUG
        }

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        response = self.client.post(ADD_URL, data=self.form_data)
        expected_url = f'{LOGIN_URL}?next={ADD_URL}'
        self.assertRedirects(response, expected_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.not_author_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.not_author)

    def test_slug_is_unique(self):
        response = self.not_author_client.post(ADD_URL, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=SLUG + WARNING
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.not_author_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(note.slug, expected_slug)


class TestNoteSlugEditDelete(Base):
    NEW_TEXT = 'Новый текст заметки'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': TITLE,
            'text': cls.NEW_TEXT,
            'slug': SLUG
        }

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_note = Note.objects.get(id=self.note.id)
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.slug, self.form_data['slug'])

    def test_author_can_delete_note(self):
        initial_notes_count = Note.objects.count()
        response = self.author_client.delete(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, initial_notes_count - 1)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.not_author_client.post(EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        new_note = Note.objects.get(id=self.note.id)
        self.assertEqual(new_note.text, self.note.text)
        self.assertEqual(new_note.title, self.note.title)
        self.assertEqual(new_note.slug, self.note.slug)

    def test_user_cant_delete_comment_of_another_user(self):
        initial_notes_count = Note.objects.count()
        response = self.not_author_client.delete(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, initial_notes_count)
