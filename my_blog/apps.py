from django.apps import AppConfig


class MyBlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_blog'

    def ready(self):
        import my_blog.signals
