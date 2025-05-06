#  Genji Blog API

Автоматизированный блог с ИИ, Make и системой уведомлений.  
Позволяет пользователям создавать посты, комментировать, ставить лайки и добавлять в избранное.

---

##  Фичи

-  Регистрация и логин по JWT-токену (Djoser + SimpleJWT)
-  CRUD для постов, комментариев, лайков, избранного
-  Поиск, сортировка и фильтрация постов
-  Экспорт постов в CSV и JSON
-  Swagger-документация (drf-spectacular)
-  Генерация `description` через OpenAI
-  GPT-автозаполнение `content`, если он не указан:
  1. Webhook отправляет `title` в Make.
  2. Make → Together.ai (GPT) → генерирует `content`.
  3. Make PATCH'ит `content` обратно в Django через Token-бота.

---

##  AI + Make: интеграция

- Используется модель `Mixtral` или `LLaMA-2` от Together.ai
- Интеграция через Make (Webhook + HTTP)
- Отправка идёт только если `content` пустой
- Обновление поста через `PATCH` и бота `make_bot`

Пример JSON запроса от Make:

```json
{
  "id": 12,
  "title": "В чем сила брат?"
}
```

Ответ GPT:

```json
{
  "content": "Сила - в правде!"
}
```

---

##  Технологии

- Python 3.11
- Django 4+
- Django REST Framework
- drf-spectacular
- Djoser + SimpleJWT
- Make (вебхуки, интеграции)
- Together.ai (через OpenAI совместимость)
- Docker (опционально)
- Pytest (опционально)

---

##  Установка

```bash
git clone https://github.com/August-Genji/gengi_blog.git
cd gengi_blog
python -m venv venv
source venv/bin/activate  # или .\venv\Scripts\activate на Windows
pip install -r requirements.txt
```

---

##  Запуск

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

📄 Swagger: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)  
📘 OpenAPI schema: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

##  .env

В проекте используется файл `.env` для конфиденциальных переменных.  
Добавлен пример `.env.example`, содержащий все необходимые ключи:

```env
# Основные настройки Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# ИИ-интеграция
WEBHOOK_URL=https://hook.eu2.make.com/your_webhook_id
TOGETHER_API_KEY=your_together_api_key
GPT_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1

# Токен бота Make
MAKE_BOT_TOKEN=your_bot_token_here

```

---

##  Тесты

```bash
pytest
```

---

##  Автор

**Аданов Август**  
GitHub: [https://github.com/August-Genji](https://github.com/August-Genji)

---

