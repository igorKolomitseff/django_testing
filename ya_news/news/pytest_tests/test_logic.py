from http import HTTPStatus
import pytest

from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment
from news.forms import WARNING


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, detail_url, form_data):
    client.post(detail_url, data=form_data)
    assert Comment.objects.count() == 0, (
        'Убедитесь, что анонимный пользователь не может отправить комментарий.'
    )


def test_user_can_create_comment(
    author_client, news, author, detail_url, url_to_comments, form_data
):
    assertRedirects(
        author_client.post(detail_url, data=form_data),
        url_to_comments,
        msg_prefix=(
            'Убедитесь, что после создания комментария авторизованный '
            'пользователь перенаправляется к разделу с комментариями.'
        )
    )
    assert Comment.objects.count() == 1, (
        'Убедитесь, что авторизированный пользователь может '
        'отправить комментарий.'
    )
    comment = Comment.objects.get()
    assert comment.text == form_data['text'], (
        'Убедитесь, что после создания комментария данные поля text '
        'объекта комментария соответствуют данным из формы.'
    )
    assert comment.news == news, (
        'Убедитесь, что после создания комментария данные поля text '
        'объекта комментария соответствуют выбранной новости.'
    )
    assert comment.author == author, (
        'Убедитесь, что данные после создания комментария данные поля author '
        'объекта комментария соответствуют объекту авторизированного '
        'пользователя.'
    )


def test_user_cant_use_bad_words(
    author_client, detail_url, bad_words_data
):
    assertFormError(
        author_client.post(detail_url, data=bad_words_data),
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0, (
        'Убедитесь, что если комментарий содержит запрещённые слова, '
        'он не будет опубликован.'
    )


def test_author_can_edit_comment(
    author_client, edit_url, form_data, url_to_comments, comment
):
    assertRedirects(
        author_client.post(edit_url, data=form_data),
        url_to_comments,
        msg_prefix=(
            'Убедитесь, что после редактирования своего комментария '
            'авторизованный пользователь перенаправляется к разделу с '
            'комментариями.'
        )
    )
    comment.refresh_from_db()
    assert comment.text == form_data['text'], (
        'Убедитесь, что после редактирования своего комментария данные '
        'поля text объекта комментария соответствуют данным из формы.'
    )


def test_user_cant_edit_comment_of_another_user(
    reader_client, edit_url, form_data, comment
):
    expected_text = comment.text
    response = reader_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что аутентифицированному пользователю недоступна страница '
        'редактирования чужого комментария.'
    )
    comment.refresh_from_db()
    assert comment.text == expected_text, (
        'Убедитесь, что аутентифицированный пользователь не может '
        'редактировать чужой комментарий.'
    )


def test_author_can_delete_comment(
    author_client, delete_url, url_to_comments
):
    assertRedirects(
        author_client.delete(delete_url),
        url_to_comments,
        msg_prefix=(
            'Убедитесь, что после удаления своего комментария '
            'авторизованный пользователь перенаправляется к разделу с '
            'комментариями.'
        )
    )
    assert Comment.objects.count() == 0, (
        'Убедитесь, что авторизированный пользователь может '
        'удалить свой комментарий.'
    )


def test_user_cant_delete_comment_of_another_user(
    reader_client, delete_url
):
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что аутентифицированному пользователю недоступна страница '
        'удаления чужого комментария.'
    )
    assert Comment.objects.count() == 1, (
        'Убедитесь, что аутентифицированный пользователь не может удалить '
        'чужой комментарий.'
    )
