# scripts/generate_bot_token.py (или где у тебя он лежит)
import os
import django

# Настройка переменной окружения ДО setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genji_blog.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def show_make_bot_token():
    bot_user, _ = User.objects.get_or_create(username='make_bot')
    token, _ = Token.objects.get_or_create(user=bot_user)
    print(f"Make Bot Token: {token.key}")

if __name__ == '__main__':
    show_make_bot_token()
