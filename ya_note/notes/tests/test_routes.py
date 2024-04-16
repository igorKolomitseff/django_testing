from http import HTTPStatus

from .configuration import TestData, Urls


class TestRoutes(TestData):

    def test_pages_availability(self):
        for url, client, status in (
            (Urls.HOMEPAGE_URL, self.client, HTTPStatus.OK),
            (Urls.LOGIN_URL, self.client, HTTPStatus.OK),
            (Urls.LOGOUT_URL, self.client, HTTPStatus.OK),
            (Urls.SIGNUP_URL, self.client, HTTPStatus.OK),
            (Urls.NOTE_ADD_URL, self.user_client, HTTPStatus.OK),
            (Urls.NOTES_LIST_URL, self.user_client, HTTPStatus.OK),
            (Urls.SUCCESS_URL, self.user_client, HTTPStatus.OK),
            (Urls.NOTE_DETAIL_URL, self.user_client, HTTPStatus.NOT_FOUND),
            (Urls.NOTE_EDIT_URL, self.user_client, HTTPStatus.NOT_FOUND),
            (Urls.NOTE_DELETE_URL, self.user_client, HTTPStatus.NOT_FOUND),
            (Urls.NOTE_ADD_URL, self.author_client, HTTPStatus.OK),
            (Urls.NOTES_LIST_URL, self.author_client, HTTPStatus.OK),
            (Urls.SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (Urls.NOTE_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (Urls.NOTE_EDIT_URL, self.author_client, HTTPStatus.OK),
            (Urls.NOTE_DELETE_URL, self.author_client, HTTPStatus.OK)
        ):
            with self.subTest(url=url, client=client, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anonymous_user(self):
        for url, redirect in (
            (Urls.NOTE_ADD_URL,
             Urls.REDIRECT_FROM_LOGIN_TO_NOTE_ADD_URL),
            (Urls.NOTES_LIST_URL,
             Urls.REDIRECT_FROM_LOGIN_TO_NOTES_LIST_URL),
            (Urls.SUCCESS_URL,
             Urls.REDIRECT_FROM_LOGIN_TO_SUCCESS_URL),
            (Urls.NOTE_DETAIL_URL,
             Urls.REDIRECT_FROM_LOGIN_TO_NOTE_DETAIL_URL),
            (Urls.NOTE_EDIT_URL,
             Urls.REDIRECT_FROM_LOGIN_TO_NOTE_EDIT_URL),
            (Urls.NOTE_DELETE_URL,
             Urls.REDIRECT_FROM_LOGIN_TO_NOTE_DELETE_URL)
        ):
            with self.subTest(url=url, redirect=redirect):
                self.assertRedirects(self.client.get(url), redirect)
