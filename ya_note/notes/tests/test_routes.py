from http import HTTPStatus

from .constants import UrlsConstants
from .set_up_test_data import TestData


class TestRoutes(TestData):

    @classmethod
    def setUpTestData(cls, create_forms_data=False):
        super().setUpTestData()

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
             UrlsConstants.REDIRECT_FROM_NOTE_ADD_TO_LOGIN_URL),
            (UrlsConstants.NOTES_LIST_URL,
             UrlsConstants.REDIRECT_FROM_NOTES_LIST_TO_LOGIN_URL),
            (UrlsConstants.SUCCESS_URL,
             UrlsConstants.REDIRECT_FROM_SUCCESS_TO_LOGIN_URL),
            (UrlsConstants.NOTE_DETAIL_URL,
             UrlsConstants.REDIRECT_FROM_NOTE_DETAIL_TO_LOGIN_URL),
            (UrlsConstants.NOTE_EDIT_URL,
             UrlsConstants.REDIRECT_FROM_NOTE_EDIT_TO_LOGIN_URL),
            (UrlsConstants.NOTE_DELETE_URL,
             UrlsConstants.REDIRECT_FROM_NOTE_DELETE_TO_LOGIN_URL)
        ):
            with self.subTest(url=url, redirect=redirect):
                self.assertRedirects(self.client.get(url), redirect)
