from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .openai_utils import generate_description


@receiver(post_save, sender=Post)
def generate_post_description(sender, instance, created, **kwargs):
    if created and not instance.description:
        instance.description = generate_description(instance.title)
        instance.save()