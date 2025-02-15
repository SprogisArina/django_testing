from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

SLUG = 'slug'
TITLE = 'Заголовок'
TEXT = 'Текст'
HOME_URL = reverse('notes:home')
ADD_URL = reverse('notes:add')
EDIT_URL = reverse('notes:edit', args=(SLUG,))
DETAIL_URL = reverse('notes:detail', args=(SLUG,))
DELETE_URL = reverse('notes:delete', args=(SLUG,))
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
User = get_user_model()


class Base(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(
            title=TITLE, text=TEXT, slug=SLUG, author=cls.author
        )
