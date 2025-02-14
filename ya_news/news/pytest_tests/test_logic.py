from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

BAD_WORDS_DATA = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


def test_anonymous_user_cant_create_comment(client, detail_url, comment_form):
    response = client.post(detail_url, data=comment_form)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={detail_url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        not_author, not_author_client, news, detail_url, comment_form
):
    response = not_author_client.post(detail_url, data=comment_form)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.news == news
    assert comment.text == comment_form['text']
    assert comment.author == not_author


def test_user_cant_use_bad_words(not_author_client, detail_url):
    response = not_author_client.post(detail_url, data=BAD_WORDS_DATA)
    assertFormError(
        response,
        'form',
        'text',
        WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client, comment_delete_url, detail_url
):
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, f'{detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(
        author_client, comment_form, comment_edit_url, detail_url, comment
):
    response = author_client.post(comment_edit_url, data=comment_form)
    assertRedirects(response, f'{detail_url}#comments')
    new_comment = Comment.objects.get(pk=comment.id)
    assert new_comment.text == comment_form['text']
    assert new_comment.news == comment.news
    assert new_comment.author == comment.author
    assert new_comment.created == comment.created


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment_delete_url
):
    response = not_author_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_user_cant_edit_comment_of_another_user(
        comment_edit_url, comment_form, not_author_client, comment
):
    response = not_author_client.post(comment_edit_url, data=comment_form)
    assert response.status_code == HTTPStatus.NOT_FOUND
    edit_comment = Comment.objects.get(id=comment.id)
    assert edit_comment.text == comment.text
    assert edit_comment.news == comment.news
    assert edit_comment.author == comment.author
    assert edit_comment.created == comment.created
