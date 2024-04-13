from http import HTTPStatus
import pytest

from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, page_name',
    (
        (pytest.lazy_fixture('home_url'),
         'домашняя страница'),
        (pytest.lazy_fixture('detail_url'),
         'страница отдельной новости'),
        (pytest.lazy_fixture('login_url'),
         'страница входа в учётную запись'),
        (pytest.lazy_fixture('logout_url'),
         'страница выхода из учётной записи'),
        (pytest.lazy_fixture('signup_url'),
         'страница регистрации'),
    )
)
def test_pages_availability_for_anonymous_user(client, url, page_name):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK, (
        f'Убедитесь, что {page_name} доступна анонимному пользователю.'
    )


@pytest.mark.parametrize(
    'parametrized_client, expected_status, user, status_name',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK,
         'автора комментария', 'доступна'),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND,
         'стороннего аутентифицированного пользователя',
         'для чужого комментария недоступна'),
    ),
)
@pytest.mark.parametrize(
    'url, page_name',
    (
        (pytest.lazy_fixture('edit_url'),
         'страница редактирования комментария'),
        (pytest.lazy_fixture('delete_url'),
         'страница удаления комментария'),
    ),
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, url, expected_status, user, status_name, page_name
):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status, (
        f'Убедитесь, что {page_name} {status_name} для {user}.'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, page_name',
    (
        (pytest.lazy_fixture('edit_url'),
         'страницу редактирования комментария'),
        (pytest.lazy_fixture('delete_url'),
         'страницу удаления комментария'),
    )
)
def test_redirect_for_anonymous_client(client, login_url, url, page_name):
    assertRedirects(
        client.get(url),
        f'{login_url}?next={url}',
        msg_prefix=(
            f'Убедитесь, что при попытке перейти на {page_name} '
            f'анонимный пользователь перенаправляется на страницу авторизации.'
        )
    )
