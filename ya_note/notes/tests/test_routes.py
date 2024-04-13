from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


NAMES_PAGES = {
    'home': ('notes:home', 'главная'),
    'login': ('users:login', 'входа в учётную запись'),
    'logout': ('users:logout', 'выхода из учётной записи'),
    'signup': ('users:signup', 'регистрации'),
    'add': ('notes:add', 'добавления новой заметки'),
    'list': ('notes:list', 'со списком заметок'),
    'success': ('notes:success', 'успешного добавления/удаления заметки'),
    'detail': ('notes:detail', 'отдельной заметки'),
    'edit': ('notes:edit', 'редактирования заметки'),
    'delete': ('notes:delete', 'удаления заметки')
}


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.authenticated_user = User.objects.create(
            username='AuthenticatedUser'
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.authenticated_client = Client()
        cls.authenticated_client.force_login(cls.authenticated_user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test',
            author=cls.author
        )
        cls.login_url = reverse('users:login')

    def test_pages_availability_for_anonymous_user(self):
        for name, page_name in (
            NAMES_PAGES['home'],
            NAMES_PAGES['login'],
            NAMES_PAGES['logout'],
            NAMES_PAGES['signup'],
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    (
                        f'Убедитесь, что страница {page_name} доступна '
                        'анонимному пользователю.'
                    )
                )

    def test_pages_availability_for_authenticated_user(self):
        for name, page_name in (
            NAMES_PAGES['add'],
            NAMES_PAGES['list'],
            NAMES_PAGES['success'],
        ):
            with self.subTest(name=name):
                response = self.authenticated_client.get(reverse(name))
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    (
                        f'Убедитесь, что страница {page_name} доступна '
                        'аутентифицированному пользователю.'
                    )
                )

    def test_availability_for_note_detail_edit_delete(self):
        for client, expected_status, user, status_name in (
                (self.author_client, HTTPStatus.OK,
                 'автору заметки', 'доступна'),
                (self.authenticated_client, HTTPStatus.NOT_FOUND,
                 'стороннему авторизированному пользователю',
                 'для чужой заметки недоступна'),
        ):
            for name, page_name in (
                    NAMES_PAGES['detail'],
                    NAMES_PAGES['edit'],
                    NAMES_PAGES['delete'],
            ):
                with self.subTest(client=client, name=name):
                    response = client.get(reverse(
                        name, args=(self.note.slug,)
                    ))
                    self.assertEqual(
                        response.status_code,
                        expected_status,
                        (
                            f'Убедитесь, что страница {page_name} '
                            f'{status_name} {user}.'
                        )
                    )

    def test_redirect_for_anonymous_client(self):
        slug = self.note.slug
        for name, page_name, args in (
            (*NAMES_PAGES['add'], None),
            (*NAMES_PAGES['list'], None),
            (*NAMES_PAGES['success'], None),
            (*NAMES_PAGES['detail'], (slug,)),
            (*NAMES_PAGES['edit'], (slug,)),
            (*NAMES_PAGES['delete'], (slug,)),
        ):
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f'{self.login_url}?next={url}',
                    msg_prefix=(
                        'Убедитесь, что при попытке перейти на страницу '
                        f'{page_name} анонимный пользователь перенаправляется '
                        'на страницу логина.'
                    )
                )
