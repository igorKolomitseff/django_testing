from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


HOMEPAGE_URL = pytest.lazy_fixture('homepage_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit_url')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')

ANONYMOUS_CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
READER_CLIENT = pytest.lazy_fixture('reader_client')

REDIRECT_FROM_LOGIN_URL_TO_COMMENT_EDIT_URL = pytest.lazy_fixture(
    'redirect_from_login_to_comment_edit_url'
)
REDIRECT_FROM_LOGIN_URL_TO_COMMENT_DELETE_URL = pytest.lazy_fixture(
    'redirect_from_login_to_comment_delete_url'
)

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (HOMEPAGE_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (LOGIN_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, READER_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE_URL, READER_CLIENT, HTTPStatus.NOT_FOUND)
    )
)
def test_pages_availability(url, parametrized_client, expected_status):
    assert parametrized_client.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_url',
    (
        (COMMENT_EDIT_URL, REDIRECT_FROM_LOGIN_URL_TO_COMMENT_EDIT_URL),
        (COMMENT_DELETE_URL, REDIRECT_FROM_LOGIN_URL_TO_COMMENT_DELETE_URL)
    )
)
def test_redirect_for_anonymous_client(client, url, expected_url):
    assertRedirects(client.get(url), expected_url)
