import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


def test_news_count(client, many_news, home_url):
    response = client.get(home_url)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, many_news, home_url):
    response = client.get(home_url)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, detail_url, many_comments):
    response = client.get(detail_url)
    assert 'news' in response.context
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    'user, form_status',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('not_author_client'), True)
    )
)
def test_different_client_has_form(detail_url, user, form_status):
    response = user.get(detail_url)
    assert isinstance(response.context.get('form'), CommentForm) == form_status
