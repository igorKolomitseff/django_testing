from notes.forms import NoteForm
from notes.models import Note
from .constants import UrlsConstants
from .set_up_test_data import TestData


class TestContent(TestData):

    @classmethod
    def setUpTestData(cls, create_forms_data=False):
        super().setUpTestData()

    def test_notes_list(self):
        self.assertIn(
            self.note,
            self.author_client.get(
                UrlsConstants.NOTES_LIST_URL
            ).context['object_list']
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_authorized_user_cant_see_notes_from_other_people(self):
        self.assertNotIn(
            self.note,
            self.authenticated_client.get(
                UrlsConstants.NOTES_LIST_URL
            ).context['object_list']
        )

    def test_pages_has_form(self):
        for url in (
            UrlsConstants.NOTE_ADD_URL,
            UrlsConstants.NOTE_EDIT_URL
        ):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
