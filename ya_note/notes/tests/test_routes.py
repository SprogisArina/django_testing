from http import HTTPStatus

from django.urls import reverse

from notes.tests.fixtures import (
    Base, HOME_URL, ADD_URL, EDIT_URL, DETAIL_URL, DELETE_URL, LIST_URL,
    SUCCESS_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL
)


class TestRoutes(Base):

    def test_pages_availability(self):
        urls = (
            HOME_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_add_done(self):
        for url in (LIST_URL, SUCCESS_URL, ADD_URL):
            with self.subTest(url=url):
                response = self.not_author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_detail_edit_and_delete(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.not_author_client, HTTPStatus.NOT_FOUND)
        )
        for user, status in users_statuses:
            for url in (DETAIL_URL, EDIT_URL, DELETE_URL):
                with self.subTest(user=user, url=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            EDIT_URL, DELETE_URL, DETAIL_URL, LIST_URL, ADD_URL, SUCCESS_URL
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{LOGIN_URL}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
