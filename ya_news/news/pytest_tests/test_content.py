import pytest
from django.conf import settings

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_news_count(client, homepage_url, a_lot_of_news):
    assert client.get(
        homepage_url
    ).context['object_list'].count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, homepage_url, a_lot_of_news):
    all_dates = [
        news.date for news in client.get(homepage_url).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, news_detail_url, a_lot_of_comments):
    response = client.get(news_detail_url)
    assert 'news' in response.context
    all_timestamps = [
        comment.created for comment in response.context.get(
            'news'
        ).comment_set.all()
    ]
    assert all_timestamps == sorted(all_timestamps)


def test_authorized_client_has_form(author_client, news_detail_url):
    assert isinstance(
        author_client.get(news_detail_url).context.get('form'),
        CommentForm
    )


def test_anonymous_client_has_no_form(client, news_detail_url):
    assert 'form' not in client.get(news_detail_url).context
