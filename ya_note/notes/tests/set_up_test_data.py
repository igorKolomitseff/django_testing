from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from .constants import SLUG
from notes.models import Note


User = get_user_model()


class TestData(TestCase):

    @classmethod
    def setUpTestData(cls, create_single_note=False):
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.authenticated_user = User.objects.create(
            username='AuthenticatedUser'
        )
        cls.authenticated_client = Client()
        cls.authenticated_client.force_login(cls.authenticated_user)
        if create_single_note:
            cls.note = Note.objects.create(
                title='Заголовок',
                text='Текст',
                slug=SLUG,
                author=cls.author
            )
