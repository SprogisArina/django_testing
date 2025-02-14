from notes.forms import NoteForm
from notes.tests.fixtures import Base, ADD_URL, EDIT_URL, LIST_URL


class TestListPage(Base):

    def test_notes_list_for_different_users(self):
        user_note_in_list = (
            (self.author_client, True),
            (self.not_author_client, False)
        )
        for user, note_in_list in user_note_in_list:
            with self.subTest(user=user):
                response = user.get(LIST_URL)
                object_list = response.context['object_list']
                self.assertIs((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        for url in (ADD_URL, EDIT_URL):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
