from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestListPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', slug='title', author=cls.author
        )

    def test_notes_list_for_different_users(self):
        user_note_in_list = (
            (self.author_client, True),
            (self.not_author_client, False)
        )
        for user, note_in_list in user_note_in_list:
            with self.subTest(client=user):
                response = user.get(reverse('notes:list'))
                object_list = response.context['object_list']
                self.assertTrue((self.note in object_list) == note_in_list)

    def test_pages_contains_form(self):
        for name, kwargs in (
            ('notes:add', None),
            ('notes:edit', {'slug': self.note.slug})
        ):
            with self.subTest(name=name, kwargs=kwargs):
                url = reverse(name, kwargs=kwargs)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
