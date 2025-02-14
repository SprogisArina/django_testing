from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')
COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit_url')
LOGIN_URL = reverse('users:login')


@pytest.mark.parametrize(
    'url',
    (HOME_URL, DETAIL_URL, LOGIN_URL,
     reverse('users:logout'), reverse('users:signup'))
)
def test_pages_availability_for_anonymous_user(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'url',
    (COMMENT_EDIT_URL, COMMENT_DELETE_URL)
)
def test_pages_availability_for_auth_user(
        parametrized_client, expected_status, url
):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (COMMENT_EDIT_URL, COMMENT_DELETE_URL)
)
def test_redirect_for_anonymous_client(client, url):
    expected_url = f'{LOGIN_URL}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
