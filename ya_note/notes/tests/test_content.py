from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note


User = get_user_model()


class TestContent(TestCase):

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

    def test_notes_list_for_different_users(self):
        for client, note_in_list_status, user, note_in_list in (
            (self.author_client, True,
             'автора заметки', 'заметка есть'),
            (self.authenticated_client, False,
             'стороннего авторизированного пользователя',
             'чужой заметки нет')
        ):
            with self.subTest(client=client):
                response = client.get(reverse('notes:list'))
                object_list = response.context['object_list']
                self.assertIs(
                    self.note in object_list,
                    note_in_list_status,
                    (
                        f'Убедитесь, что {note_in_list} в контексте страницы '
                        f'со списком заметок для {user}.'
                    )
                )

    def test_pages_has_form(self):
        for name, page_name, args in (
            ('notes:add', 'добавления новой заметки', None),
            ('notes:edit', 'редактирования заметки', (self.note.slug,))
        ):
            with self.subTest(name=name):
                response = self.author_client.get(reverse(name, args=args))
                self.assertIn(
                    'form',
                    response.context,
                    (
                        'Убедитесь, что объект form есть в словаре '
                        f'контекста для страницы {page_name}.'
                    )
                )
                self.assertIsInstance(
                    response.context['form'],
                    NoteForm,
                    (
                        'Убедитесь, что объект form относится к классу '
                        'NoteForm.'
                    )
                )
