import openai

from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def generate_description(prompt):
    # Фейковый заглушечный ответ для демонстрации
    return f"AI-сгенерированное описание на тему: {prompt}"

    # Реальная реализация (если будет нужно)
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "Ты помощник, который генерирует описания к постам."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return response.choices[0].message["content"]