from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from .constants import SLUG
from notes.models import Note


User = get_user_model()


class TestData(TestCase):

    @classmethod
    def setUpTestData(cls, create_forms_data=False):
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.authenticated_user = User.objects.create(
            username='AuthenticatedUser'
        )
        cls.authenticated_client = Client()
        cls.authenticated_client.force_login(cls.authenticated_user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=SLUG,
            author=cls.author
        )
        if create_forms_data:
            cls.create_note_form_data = {
                'title': 'Новый заголовок',
                'text': 'Новый текст',
                'slug': 'new_note'
            }
            cls.edit_note_form_data = {
                'title': 'Изменённый заголовок',
                'text': 'Изменённый текст',
                'slug': 'edit_note'
            }
