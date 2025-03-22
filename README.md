# Vice Versa

Проект предназначен для изучения библиотек тестирования: Pytest и unittest

## Функции проекта

Для тестирования используются два готовых проекта:
1. YaNews - новостной сайт.
2. YaNote - сервис электронных заметок.

Тесты разделены на следующие категории:
* тестирование маршрутов: доступ к эндпоинтам, проверка редиректов, кодов 
ответа, доступ страниц для анонимных и авторизированных пользователей.
* тестирование контента: правильность отображение данных, корректность работы 
пагинации.
* тестирование бизнес-логики.

Для тестирования YaNews использовал библиотеку Pytest, для тестирования YaNote - unittest.

## Стек технологий
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [SQLite](https://www.sqlite.org/)
* [HTML](https://developer.mozilla.org/ru/docs/Web/HTML)
* [CSS](https://developer.mozilla.org/ru/docs/Web/CSS)
* [Bootstrap](https://getbootstrap.com/)
* [Pytest](https://docs.pytest.org/en/stable/)
* [unittest](https://docs.python.org/3/library/unittest.html)

## Как развернуть проект
1. Клонируйте репозиторий и перейдите в директорию django_testing
```bash
git clone git@github.com:igorKolomitseff/django_testing.git
cd django_testing
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux и macOS
source venv/Scripts/activate  # Для Windows
```

3. Обновите pip и установите зависимости проекта:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Для изучения проекта YaNews:

1. Перейдите в директорию ya_news и примените миграции:
```bash
cd ya_news/
python3 manage.py migrate
```

2. Загрузите подготовленные данные (фикстуру) в базу данных:
```bash
python3 manage.py loaddata news/fixtures/news.json
```

3. Создайте суперпользователя, укажите запрашиваемые данные:
```bash
python3 manage.py createsuperuser
```

4. Запустите проект:
```bash
python3 manage.py runserver
```

Откройте браузер и перейдите по адресу 
[http://127.0.0.1:8000/](http://127.0.0.1:8000/) для доступа главной странице 
проекта и [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) для 
доступа к административной панели

Команда для запуска тестов:
```bash
pytest
```

---

Для изучения проекта YaNote:

1. Перейдите в директорию ya_note и примените миграции:
```bash
cd ya_note/
python3 manage.py migrate
```

2. Создайте суперпользователя, укажите запрашиваемые данные:
```bash
python3 manage.py createsuperuser
```

3. Запустите проект:
```bash
python3 manage.py runserver
```

Откройте браузер и перейдите по адресу 
[http://127.0.0.1:8000/](http://127.0.0.1:8000/) для доступа главной странице 
проекта и [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) для 
доступа к административной панели

Команда для запуска тестов:
```bash
python3 manage.py test
```

### Автор

[Игорь Коломыцев](https://github.com/igorKolomitseff)
