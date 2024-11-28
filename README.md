# AtomChat API

API атом чата, в котором пользователи могут общаться друг с другом в приватных каналах.

## Возможности AtomChat API

- Регистрация новых пользователей и авторизация
- Предусмотрена роль модератора, которому доступны все каналы и предоставлена возможность блокировки пользователей
- Сообщения отправляются в режиме "реального времени"
- Пользователям доступен функционал просмотра истории сообщений

## Технологии

- python 3.10+ - высокоуровневый язык программирования общего назначения
- django 5.1.3 - фреймворк для веб-приложений на языке Python
- djangorestframework 3.15.2 - фреймворк для разработки веб-API в приложениях на основе Django
- psycopg2-binary 2.9.10 - библиотека взаимодействия с СУБД PostgreSQL

## Установка на локальной машине

1. Клонировать репозиторий c GitHub
```
$ git clone https://github.com/Le0har/AtomChat
```
2. Создать виртуальное окружение
```
$ python3 -m venv django_venv
```
3. Запустить виртуальное окружение
```
$ source django_venv/bin/activate
```
4. Обновить менеджер пакетов pip
```
$ python -m pip install --upgrade pip
```
5. Установить зависимости из ```requirements.txt```
```
$ pip install -r requirements.txt
```
6. Настроить подключение к БД (PostgreSQL) в файле ```settings.py```

- `ENGINE` - механизм, который используется для поключения к БД. В данном проекте - `django.db.backends.postgresql_psycopg2`
- `NAME` - имя БД
- `USER` - имя пользователя для подключения к БД
- `PASSWORD` - пароль для подключения к БД
- `HOST` - хост, на котором располагается БД. В данном проекте - `localhost`
- `PORT` - порт подключения к БД. В данном проекте - `5432`

7. Выполнить миграции
```
$ python manage.py migrate
```
8. Запустить проект
```
$ python manage.py runserver
```

## Примеры запросов

- POST: http://<span></span>127.0.0.1:8000/api/users/

Response:

```J-SON
{
  "username": "valentin",
  "password": "user_val99",
  "email": "valentin99@ati.hom"
}
```

Request:

```J-SON
{
  "email": "valentin99@ati.hom",
  "username": "valentin"
}
```

- POST: http://<span></span>127.0.0.1:8000/api/auth/tokens/

Response:

```J-SON
{
  "username": "valentin",
  "password": "user_val99"
}
```

Request:

```J-SON
{
  "token": "1f3d6a1986645c7338c7cc66c0a615b26bd1e828"
}
```

- GET: http://<span></span>127.0.0.1:8000/api/rooms/

Request:

```J-SON
[
  {
    "id": 9,
    "name": "ivan&petya_private",
    "is_private": true,
    "created_at": "2024-11-21T05:51:01.115398Z",
    "users": [
      2,
      3
    ]
  },
  {
    "id": 17,
    "name": "Разговоры о погоде",
    "is_private": true,
    "created_at": "2024-11-21T14:13:13.480149Z",
    "users": [
      2,
      3,
      4
    ]
  }
]
```

- GET: http://<span></span>127.0.0.1:8000/api/rooms/17/messages/

Request:

```J-SON
[
  {
    "text": "А завтра ожидается снег?",
    "created_at": "2024-11-22T08:58:29.843174Z",
    "author": 3
  },
  {
    "text": "И послезавтра тоже ожидается снег",
    "created_at": "2024-11-22T09:02:05.395774Z",
    "author": 2
  }
]
```

- POST: http://<span></span>127.0.0.1:8000/api/rooms/17/messages/

Response:

```J-SON
{
  "text": "Как много снега намело!"
}
```

Request:

```J-SON
[
  {
    "text": "А завтра ожидается снег?",
    "created_at": "2024-11-22T08:58:29.843174Z",
    "author": 3
  },
  {
    "text": "И послезавтра тоже ожидается снег",
    "created_at": "2024-11-22T09:02:05.395774Z",
    "author": 2
  },
  {
    "text": "Как много снега намело!",
    "created_at": "2024-11-22T18:09:34.480149Z",
    "author": 4
  }
]
```


## Автор

Тихонов Алексей [https://github.com/Le0har](https://github.com/Le0har)