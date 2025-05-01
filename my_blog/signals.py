from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, PostWorkFlow
from .openai_utils import generate_description


@receiver(post_save, sender=Post)
def generate_post_description(sender, instance, created, **kwargs):
    if created and not instance.description:
        instance.description = generate_description(instance.title)
        instance.save()

@receiver(post_save, sender=Post)
def handle_post_workflow(sender, instance, created, **kwargs):
    print("Я СРАБОТАЛ!!!!!!!!!!!!!!!!!!!!!!!")
    if created:
        print("ПОСТ СОЗДАНАААААААААААААААААААААА")
        PostWorkFlow.objects.create(post=instance, step='created')
        if not instance.description:
            description = generate_post_description(instance.title)
            instance.description = description
            instance.save()

            PostWorkFlow.objects.create(post=instance, step="ai_description", note=f"Generated description {description[:50]}")

        elif len(instance.content) > 100:
            instance.status = 'popular'
            instance.save()

            PostWorkFlow.objects.create(post=instance, step="marked_popular", note="Content length > 100")
