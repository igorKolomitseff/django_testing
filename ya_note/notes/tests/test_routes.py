from http import HTTPStatus

from .constants import UrlsConstants
from .set_up_test_data import TestData


class TestRoutes(TestData):

    @classmethod
    def setUpTestData(cls, create_single_note=False):
        super().setUpTestData(create_single_note=True)

    def test_pages_availability(self):
        for url, client, status in (
            (UrlsConstants.HOMEPAGE_URL,
             self.client,
             HTTPStatus.OK),
            (UrlsConstants.LOGIN_URL,
             self.client,
             HTTPStatus.OK),
            (UrlsConstants.LOGOUT_URL,
             self.client,
             HTTPStatus.OK),
            (UrlsConstants.SIGNUP_URL,
             self.client,
             HTTPStatus.OK),
            (UrlsConstants.NOTE_ADD_URL,
             self.authenticated_client,
             HTTPStatus.OK),
            (UrlsConstants.NOTES_LIST_URL,
             self.authenticated_client,
             HTTPStatus.OK),
            (UrlsConstants.SUCCESS_URL,
             self.authenticated_client,
             HTTPStatus.OK),
            (UrlsConstants.NOTE_DETAIL_URL,
             self.author_client,
             HTTPStatus.OK),
            (UrlsConstants.NOTE_EDIT_URL,
             self.author_client,
             HTTPStatus.OK),
            (UrlsConstants.NOTE_DELETE_URL,
             self.author_client,
             HTTPStatus.OK),
            (UrlsConstants.NOTE_DETAIL_URL,
             self.authenticated_client,
             HTTPStatus.NOT_FOUND),
            (UrlsConstants.NOTE_EDIT_URL,
             self.authenticated_client,
             HTTPStatus.NOT_FOUND),
            (UrlsConstants.NOTE_DELETE_URL,
             self.authenticated_client,
             HTTPStatus.NOT_FOUND)
        ):
            with self.subTest(url=url, client=client, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anonymous_user(self):
        for url, redirect in (
            (UrlsConstants.NOTE_ADD_URL,
             UrlsConstants.REDIRECT_TO_NOTE_ADD_URL),
            (UrlsConstants.NOTES_LIST_URL,
             UrlsConstants.REDIRECT_TO_NOTES_LIST_URL),
            (UrlsConstants.SUCCESS_URL,
             UrlsConstants.REDIRECT_TO_SUCCESS_URL),
            (UrlsConstants.NOTE_DETAIL_URL,
             UrlsConstants.REDIRECT_TO_NOTE_DETAIL_URL),
            (UrlsConstants.NOTE_EDIT_URL,
             UrlsConstants.REDIRECT_TO_NOTE_EDIT_URL),
            (UrlsConstants.NOTE_DELETE_URL,
             UrlsConstants.REDIRECT_TO_NOTE_DELETE_URL)
        ):
            with self.subTest(url=url, redirect=redirect):
                self.assertRedirects(self.client.get(url), redirect)
