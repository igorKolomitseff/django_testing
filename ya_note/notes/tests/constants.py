from django.urls import reverse


SLUG = 'test'


class ConstantsUrls():
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

    REDIRECT_TO_NOTE_ADD_URL = f'{LOGIN_URL}?next={NOTE_ADD_URL}'
    REDIRECT_TO_NOTES_LIST_URL = f'{LOGIN_URL}?next={NOTES_LIST_URL}'
    REDIRECT_TO_SUCCESS_URL = f'{LOGIN_URL}?next={SUCCESS_URL}'
    REDIRECT_TO_NOTE_DETAIL_URL = f'{LOGIN_URL}?next={NOTE_DETAIL_URL}'
    REDIRECT_TO_NOTE_EDIT_URL = f'{LOGIN_URL}?next={NOTE_EDIT_URL}'
    REDIRECT_TO_NOTE_DELETE_URL = f'{LOGIN_URL}?next={NOTE_DELETE_URL}'
