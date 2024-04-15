from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError
import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


CREATE_COMMENT_FORM_DATA = {
    'text': 'Новый текст комментария'
}
EDIT_COMMENT_FORM_DATA = {
    'text': 'Изменённый текст комментария'
}

pytestmark = pytest.mark.django_db


def get_bad_words_data(bad_word):
    return {
        'text': f'Текст, {bad_word}, больше текста'
    }


def test_anonymous_user_cant_create_comment(client, news_detail_url):
    initial_comments = set(Comment.objects.all())
    client.post(news_detail_url, data=CREATE_COMMENT_FORM_DATA)
    assert set(Comment.objects.all()) == initial_comments


def test_user_can_create_comment(
    author_client, news, author, news_detail_url, redirect_to_comments_url
):
    initial_comments = set(Comment.objects.all())
    assertRedirects(
        author_client.post(news_detail_url, data=CREATE_COMMENT_FORM_DATA),
        redirect_to_comments_url)
    changing_db = set(Comment.objects.all()) - initial_comments
    assert len(changing_db) == 1
    new_comment = changing_db.pop()
    assert new_comment.text == CREATE_COMMENT_FORM_DATA['text']
    assert new_comment.news == news
    assert new_comment.author == author


@pytest.mark.parametrize(
    'bad_word',
    BAD_WORDS
)
def test_user_cant_use_bad_words(
    author_client, news_detail_url, bad_word
):
    initial_comments = set(Comment.objects.all())
    assertFormError(
        author_client.post(news_detail_url, data=get_bad_words_data(bad_word)),
        form='form',
        field='text',
        errors=WARNING
    )
    assert set(Comment.objects.all()) == initial_comments


def test_author_can_edit_comment(
    author_client, comment_edit_url, redirect_to_comments_url, comment
):
    assertRedirects(
        author_client.post(comment_edit_url, data=EDIT_COMMENT_FORM_DATA),
        redirect_to_comments_url
    )
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == EDIT_COMMENT_FORM_DATA['text']
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author


def test_user_cant_edit_comment_of_another_user(
    reader_client, comment_edit_url, comment, news, author
):
    expected_text = comment.text
    response = reader_client.post(
        comment_edit_url,
        data=EDIT_COMMENT_FORM_DATA
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == expected_text
    assert comment.news == news
    assert comment.author == author


def test_author_can_delete_comment(
    author_client, comment_delete_url, redirect_to_comments_url
):
    initial_number_of_comments = Comment.objects.count()
    assertRedirects(
        author_client.delete(comment_delete_url),
        redirect_to_comments_url
    )
    assert Comment.objects.count() == initial_number_of_comments - 1


def test_user_cant_delete_comment_of_another_user(
    reader_client, comment_delete_url
):
    initial_comments = set(Comment.objects.all())
    response = reader_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert set(Comment.objects.all()) == initial_comments
