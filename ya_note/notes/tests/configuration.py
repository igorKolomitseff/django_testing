from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()

SLUG = 'test'


class Urls:
    HOMEPAGE_URL = reverse('notes:home')
    LOGIN_URL = reverse('users:login')
    LOGOUT_URL = reverse('users:logout')
    SIGNUP_URL = reverse('users:signup')
    NOTE_ADD_URL = reverse('notes:add')
    NOTES_LIST_URL = reverse('notes:list')
    SUCCESS_URL = reverse('notes:success')
    NOTE_DETAIL_URL = reverse('notes:detail', args=(SLUG,))
    NOTE_EDIT_URL = reverse('notes:edit', args=(SLUG,))
    NOTE_DELETE_URL = reverse('notes:delete', args=(SLUG,))

    REDIRECT_FROM_LOGIN_TO_NOTE_ADD_URL = (
        f'{LOGIN_URL}?next={NOTE_ADD_URL}'
    )
    REDIRECT_FROM_LOGIN_TO_NOTES_LIST_URL = (
        f'{LOGIN_URL}?next={NOTES_LIST_URL}'
    )
    REDIRECT_FROM_LOGIN_TO_SUCCESS_URL = (
        f'{LOGIN_URL}?next={SUCCESS_URL}'
    )
    REDIRECT_FROM_LOGIN_TO_NOTE_DETAIL_URL = (
        f'{LOGIN_URL}?next={NOTE_DETAIL_URL}'
    )
    REDIRECT_FROM_LOGIN_TO_NOTE_EDIT_URL = (
        f'{LOGIN_URL}?next={NOTE_EDIT_URL}'
    )
    REDIRECT_FROM_LOGIN_TO_NOTE_DELETE_URL = (
        f'{LOGIN_URL}?next={NOTE_DELETE_URL}'
    )


class TestData(TestCase):

    @classmethod
    def setUpTestData(cls, create_forms_data=False):
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = User.objects.create(username='User')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
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
