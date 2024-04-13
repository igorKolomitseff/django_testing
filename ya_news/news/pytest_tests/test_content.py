import pytest

from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
@pytest.mark.usefixtures('a_lot_of_news')
def test_news_count(client, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE, (
        f'Убедитесь, что количество новостей на главной странице — '
        f'не более {settings.NEWS_COUNT_ON_HOME_PAGE}.'
    )


@pytest.mark.django_db
@pytest.mark.usefixtures('a_lot_of_news')
def test_news_order(client, home_url):
    response = client.get(home_url)
    all_dates = [news.date for news in response.context['object_list']]
    assert all_dates == sorted(all_dates, reverse=True), (
        'Убедитесь, что новости отсортированы от самой свежей к самой старой.'
    )


@pytest.mark.django_db
@pytest.mark.usefixtures('a_lot_of_comments')
def test_comments_order(client, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context, (
        'Убедитесь, что объект новости находится в словаре контекста'
        'под ожидаемым именем - названием модели News.'
    )
    news = response.context['news']
    all_timestamps = [
        comment.created for comment in news.comment_set.all()
    ]
    assert all_timestamps == sorted(all_timestamps), (
        'Убедитесь, что комментарии на странице отдельной новости '
        'отсортированы в хронологическом порядке: '
        'старые в начале списка, новые — в конце.'
    )


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context, (
        'Убедитесь, что авторизированному пользователю доступна форма для '
        'отправки комментария на странице отдельной новости.'
    )
    assert isinstance(response.context['form'], CommentForm), (
        'Убедитесь, что объект формы соответствует классу CommentForm.'
    )


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context, (
        'Убедитесь, что анонимному пользователю недоступна форма для отправки '
        'комментария на странице отдельной новости.'
    )
