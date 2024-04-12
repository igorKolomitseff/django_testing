from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


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

    def test_pages_availability_for_anonymous_user(self):
        for name, page_name in (
            ('notes:home', 'главная'),
            ('users:login', 'входа в учётную запись'),
            ('users:logout', 'выхода из учётной записи'),
            ('users:signup', 'регистрации'),
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
            ('notes:add', 'добавления новой заметки'),
            ('notes:list', 'со списком заметок'),
            ('notes:success', 'успешного добавления/удаления заметки'),
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
                 'стороннему аутентифицированному пользователю', 'недоступна'),
        ):
            for name, page_name in (
                    ('notes:detail', 'отдельной заметки'),
                    ('notes:edit', 'редактирования заметки'),
                    ('notes:delete', 'удаления заметки'),
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
        login_url = reverse('users:login')
        slug = self.note.slug
        for name, page_name, args in (
            ('notes:add', 'добавления новой заметки', None),
            ('notes:list', 'со списком заметок', None),
            ('notes:success', 'успешного добавления/удаления заметки', None),
            ('notes:detail', 'отдельной заметки', (slug,)),
            ('notes:edit', 'редактирования заметки', (slug,)),
            ('notes:delete', 'удаления заметки', (slug,)),
        ):
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    redirect_url,
                    msg_prefix=(
                        'Убедитесь, что при попытке перейти на страницу '
                        f'{page_name} анонимный пользователь перенаправляется '
                        'на страницу логина.'
                    )
                )
