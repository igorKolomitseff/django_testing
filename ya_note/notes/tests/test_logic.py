from http import HTTPStatus

from pytils.translit import slugify

from .configuration import TestData, Urls
from notes.forms import WARNING
from notes.models import Note


class TestLogic(TestData):

    @classmethod
    def setUpTestData(cls, create_forms_data=True):
        super().setUpTestData(create_forms_data=True)

    def test_anonymous_user_cant_create_note(self):
        initial_notes = Note.objects.all()
        self.assertRedirects(
            self.client.post(
                Urls.NOTE_ADD_URL,
                data=self.create_note_form_data
            ),
            Urls.REDIRECT_FROM_LOGIN_TO_NOTE_ADD_URL,
        )
        self.assertQuerysetEqual(Note.objects.all(), initial_notes)

    def test_user_can_create_note(self):
        initial_notes = set(Note.objects.all())
        self.assertRedirects(
            self.author_client.post(
                Urls.NOTE_ADD_URL,
                data=self.create_note_form_data
            ),
            Urls.SUCCESS_URL
        )
        changing_db = set(Note.objects.all()) - initial_notes
        self.assertEqual(len(changing_db), 1)
        new_note = changing_db.pop()
        self.assertEqual(new_note.title, self.create_note_form_data['title'])
        self.assertEqual(new_note.text, self.create_note_form_data['text'])
        self.assertEqual(new_note.slug, self.create_note_form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_not_unique_slug(self):
        initial_notes = Note.objects.all()
        self.create_note_form_data['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(
                Urls.NOTE_ADD_URL,
                data=self.create_note_form_data
            ),
            form='form',
            field='slug',
            errors=(self.create_note_form_data['slug'] + WARNING)
        )
        self.assertQuerysetEqual(Note.objects.all(), initial_notes)

    def test_empty_slug(self):
        initial_notes = set(Note.objects.all())
        self.create_note_form_data.pop('slug')
        self.assertRedirects(
            self.author_client.post(
                Urls.NOTE_ADD_URL,
                data=self.create_note_form_data),
            Urls.SUCCESS_URL
        )
        changing_db = set(Note.objects.all()) - initial_notes
        self.assertEqual(len(changing_db), 1)
        new_note = changing_db.pop()
        self.assertEqual(new_note.title, self.create_note_form_data['title'])
        self.assertEqual(new_note.text, self.create_note_form_data['text'])
        self.assertEqual(
            new_note.slug,
            slugify(self.create_note_form_data['title'])
        )
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        self.assertRedirects(
            self.author_client.post(
                Urls.NOTE_EDIT_URL,
                self.edit_note_form_data),
            Urls.SUCCESS_URL
        )
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.edit_note_form_data['title'])
        self.assertEqual(note_from_db.text, self.edit_note_form_data['text'])
        self.assertEqual(note_from_db.slug, self.edit_note_form_data['slug'])
        self.assertEqual(note_from_db.author, self.author)

    def test_another_user_cant_edit_note(self):
        self.assertEqual(
            self.user_client.post(
                Urls.NOTE_EDIT_URL,
                self.edit_note_form_data
            ).status_code,
            HTTPStatus.NOT_FOUND
        )
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)

    def test_author_can_delete_note(self):
        initial_number_of_notes = Note.objects.count()
        self.assertRedirects(
            self.author_client.delete(Urls.NOTE_DELETE_URL),
            Urls.SUCCESS_URL
        )
        self.assertEqual(Note.objects.count(), initial_number_of_notes - 1)

    def test_another_user_cant_delete_note(self):
        initial_notes = Note.objects.all()
        self.assertEqual(
            self.user_client.delete(
                Urls.NOTE_DELETE_URL
            ).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertQuerysetEqual(Note.objects.all(), initial_notes)
