# Genji Blog API

Автоматизированный блог с ИИ, Make и системой уведомлений.  
Позволяет пользователям создавать посты, комментировать, ставить лайки и добавлять в избранное.

## Фичи

- Регистрация и логин по JWT-токену (Djoser + SimpleJWT)
- CRUD для постов, комментариев, лайков, избранного
- Сортировка, поиск и фильтрация постов
- Экспорт постов в CSV и JSON
- Swagger-документация (drf-spectacular)
- Генерация описания поста через OpenAI (при пустом поле `description`)
- Права доступа: `IsOwnerOrReadOnly`, `IsAdminUser`, `IsAuthenticated`

## Технологии

- Python 3.11
- Django 4+
- Django REST Framework
- drf-spectacular
- Djoser + SimpleJWT
- Make (интеграции)
- OpenAI API
- Docker (опционально)

## Установка

```bash
git clone https://github.com/August-Genji/gengi_blog.git
cd genji-blog
python -m venv venv
source venv/bin/activate  # или .\venv\Scripts\activate на Windows
pip install -r requirements.txt
```

## Запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Документация API

- Swagger: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- OpenAPI schema: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## Автор: Аданов Август  
GitHub: [https://github.com/August-Genji](https://github.com/August-Genji)