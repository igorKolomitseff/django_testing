from http import HTTPStatus

from .constants import ConstantsUrls
from .set_up_test_data import TestData


class TestRoutes(TestData):

    @classmethod
    def setUpTestData(cls, create_single_note=False):
        super().setUpTestData(create_single_note=True)

    def test_pages_availability(self):
        for url, client, status in (
            (ConstantsUrls.HOMEPAGE_URL,
             self.client,
             HTTPStatus.OK),
            (ConstantsUrls.LOGIN_URL,
             self.client,
             HTTPStatus.OK),
            (ConstantsUrls.LOGOUT_URL,
             self.client,
             HTTPStatus.OK),
            (ConstantsUrls.SIGNUP_URL,
             self.client,
             HTTPStatus.OK),
            (ConstantsUrls.NOTE_ADD_URL,
             self.authenticated_client,
             HTTPStatus.OK),
            (ConstantsUrls.NOTES_LIST_URL,
             self.authenticated_client,
             HTTPStatus.OK),
            (ConstantsUrls.SUCCESS_URL,
             self.authenticated_client,
             HTTPStatus.OK),
            (ConstantsUrls.NOTE_DETAIL_URL,
             self.author_client,
             HTTPStatus.OK),
            (ConstantsUrls.NOTE_EDIT_URL,
             self.author_client,
             HTTPStatus.OK),
            (ConstantsUrls.NOTE_DELETE_URL,
             self.author_client,
             HTTPStatus.OK),
            (ConstantsUrls.NOTE_DETAIL_URL,
             self.authenticated_client,
             HTTPStatus.NOT_FOUND),
            (ConstantsUrls.NOTE_EDIT_URL,
             self.authenticated_client,
             HTTPStatus.NOT_FOUND),
            (ConstantsUrls.NOTE_DELETE_URL,
             self.authenticated_client,
             HTTPStatus.NOT_FOUND)
        ):
            with self.subTest(url=url, client=client, status=status):
                response = client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_user(self):
        for url, redirect in (
            (ConstantsUrls.NOTE_ADD_URL,
             ConstantsUrls.REDIRECT_TO_NOTE_ADD_URL),
            (ConstantsUrls.NOTES_LIST_URL,
             ConstantsUrls.REDIRECT_TO_NOTES_LIST_URL),
            (ConstantsUrls.SUCCESS_URL,
             ConstantsUrls.REDIRECT_TO_SUCCESS_URL),
            (ConstantsUrls.NOTE_DETAIL_URL,
             ConstantsUrls.REDIRECT_TO_NOTE_DETAIL_URL),
            (ConstantsUrls.NOTE_EDIT_URL,
             ConstantsUrls.REDIRECT_TO_NOTE_EDIT_URL),
            (ConstantsUrls.NOTE_DELETE_URL,
             ConstantsUrls.REDIRECT_TO_NOTE_DELETE_URL)
        ):
            with self.subTest(url=url, redirect=redirect):
                self.assertRedirects(self.client.get(url), redirect)
