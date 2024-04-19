# Платформа для публикации платного контента

## Задача

- Реализовать платформу для публикации записей пользователями.

- Публикация может быть бесплатной, то есть доступной любому пользователю без регистрации, либо платной, которая
  доступна только авторизованным пользователям, которые оплатили разовую подписку. Для реализации оплаты подписки
  используйте Stripe. Регистрация пользователя должна быть по номеру телефона.

## Для реализации смс-отправки необходимо получить api-ключ (https://notisend.ru)


- Реализовать платформу для публикации записей пользователями.

- Публикация может быть бесплатной, то есть доступной любому пользователю без регистрации, либо платной, которая
  доступна только авторизованным пользователям, которые оплатили разовую подписку. Для реализации оплаты подписки
  используйте Stripe. Регистрация пользователя должна быть по номеру телефона.

## Технологии

- Django
- Python
- Stripe
- PostgreSQL
- Docker
- Docker Compose
- Bootstrap

## Запуск локально

- Склонировать репозиторий:
  git clone
- Создать виртуальное окружение:
  python -m venv venv
- Активировать виртуальное окружение:
  source venv/bin/activate
- Установить зависимости:
  pip install -r requirements.txt
- Прописать настройки в `.env` - `.env.sample`
- Применить миграции
  python manage.py migrate
- Запустить сервер
  python manage.py runserver

## Запуск в контейнере

- Запустить контейнер:
  `docker-compose build`
  `docker-compose up`
  или
  `docker-compose up -d`
