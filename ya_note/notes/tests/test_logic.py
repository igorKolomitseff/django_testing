from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
            'slug': 'test'
        }
        cls.add_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')

    def test_anonymous_user_cant_create_note(self):
        response = self.client.post(self.add_url, data=self.form_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={self.add_url}'
        self.assertRedirects(
            response,
            expected_url,
            msg_prefix=(
                'Убедитесь, что при попытке создать заметку анонимный '
                'пользователь перенаправляется на страницу авторизации.'
            )
        )
        self.assertEqual(
            Note.objects.count(),
            0,
            (
                'Убедитесь, что анонимный пользователь не может '
                'создать заметку.'
            )
        )

    def test_user_can_create_note(self):
        response = self.author_client.post(
            self.add_url,
            data=self.form_data
        )
        self.assertRedirects(
            response,
            self.success_url,
            msg_prefix=(
                'Убедитесь, что после создания заметки её автор '
                'перенаправляется на страницу успешного добавления заметки.'
            )
        )
        self.assertEqual(
            Note.objects.count(),
            1,
            (
                'Убедитесь, что аутентифицированный пользователь может '
                'создать заметку.'
            )
        )
        new_note = Note.objects.get()
        self.assertEqual(
            new_note.title,
            self.form_data['title'],
            (
                'Убедитесь, что данные поля title объекта заметки '
                'соответствуют данным из формы.'
            )
        )
        self.assertEqual(
            new_note.text,
            self.form_data['text'],
            (
                'Убедитесь, что данные поля text объекта заметки '
                'соответствуют данным из формы.'
            )
        )
        self.assertEqual(
            new_note.slug,
            self.form_data['slug'],
            (
                'Убедитесь, что данные поля slug объекта заметки '
                'соответствуют данным из формы.'
            )
        )
        self.assertEqual(
            new_note.author,
            self.author,
            (
                'Убедитесь, что данные поля author объекта заметки '
                'соответствуют объекту авторизированного пользователя.'
            )
        )

    def test_not_unique_slug(self):
        note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test',
            author=self.author
        )
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=(note.slug + WARNING)
        )
        self.assertEqual(
            Note.objects.count(),
            1,
            (
                'Убедитесь, что невозможно создать две заметки '
                'с одинаковым slug.'
            )
        )

    def test_empty_slug(self):
        self.form_data.pop('slug')
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertRedirects(
            response,
            self.success_url,
            msg_prefix=(
                'Убедитесь, что после создания заметки её автор '
                'перенаправляется на страницу успешного добавления заметки.'
            )
        )
        self.assertEqual(
            Note.objects.count(),
            1,
            (
                'Убедитесь, что существует возможность создания заметки '
                'с пустым полем slug.'
            )
        )
        self.assertEqual(
            Note.objects.get().slug,
            slugify(self.form_data['title']),
            (
                'Убедитесь, что если при создании заметки не заполнен slug, '
                'то он формируется автоматически, с помощью функции '
                'pytils.translit.slugify.'
            )
        )


class NoteEditDelete(TestCase):

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
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'NewTest'
        }
        cls.success_url = reverse('notes:success')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_url, self.form_data)
        self.assertRedirects(
            response,
            self.success_url,
            msg_prefix=(
                'Убедитесь, что после изменения заметки её автор '
                'перенаправляется на страницу успешного добавления заметки.'
            )
        )
        self.note.refresh_from_db()
        self.assertEqual(
            self.note.title,
            self.form_data['title'],
            (
                'Убедитесь, что данные поля title объекта заметки '
                'соответствуют данным из формы.'
            )
        )
        self.assertEqual(
            self.note.text,
            self.form_data['text'],
            (
                'Убедитесь, что данные поля text объекта заметки '
                'соответствуют данным из формы.'
            )
        )
        self.assertEqual(
            self.note.slug,
            self.form_data['slug'],
            (
                'Убедитесь, что данные поля slug объекта заметки '
                'соответствуют данным из формы.'
            )
        )

    def test_other_user_cant_edit_note(self):
        response = self.authenticated_client.post(
            self.edit_url,
            self.form_data
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND,
            (
                'Убедитесь, что авторизированному пользователю недоступна '
                'страница редактирования чужой записи.'
            )
        )
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(
            self.note.title,
            note_from_db.title,
            (
                'Убедитесь, что данные поля title объекта заметки '
                'не изменилось.'
            )
        )
        self.assertEqual(
            self.note.text,
            note_from_db.text,
            (
                'Убедитесь, что данные поля text объекта заметки '
                'не изменилось.'
            )
        )
        self.assertEqual(
            self.note.slug,
            note_from_db.slug,
            (
                'Убедитесь, что данные поля slug объекта заметки '
                'не изменилось.'
            )
        )

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(
            response,
            self.success_url,
            msg_prefix=(
                'Убедитесь, что после изменения заметки её автор '
                'перенаправляется на страницу успешного удаления заметки.'
            )
        )
        self.assertEqual(
            Note.objects.count(),
            0,
            (
                'Убедитесь, что авторизированный пользователь может '
                'удалить свою заметку.'
            )
        )

    def test_other_user_cant_delete_note(self):
        response = self.authenticated_client.delete(self.delete_url)
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND,
            (
                'Убедитесь, что авторизированному пользователю недоступна '
                'страница удаления чужой записи.'
            )
        )
        self.assertEqual(
            Note.objects.count(),
            1,
            (
                'Убедитесь, что авторизированный пользователь не может '
                'удалить чужую заметку.'
            )
        )
