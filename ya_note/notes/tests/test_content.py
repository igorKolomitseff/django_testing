from .configuration import TestData, Urls
from notes.forms import NoteForm
from notes.models import Note


class TestContent(TestData):

    def test_notes_list(self):
        notes = self.author_client.get(
            Urls.NOTES_LIST_URL
        ).context.get('object_list')
        self.assertIn(self.note, notes)
        note = notes[0]
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_another_user_cant_see_notes_from_other_people(self):
        self.assertNotIn(
            self.note,
            self.user_client.get(
                Urls.NOTES_LIST_URL
            ).context.get('object_list')
        )

    def test_pages_has_form(self):
        for url in (
            Urls.NOTE_ADD_URL,
            Urls.NOTE_EDIT_URL
        ):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
