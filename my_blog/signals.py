from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Post, PostWorkFlow, Comment
from .openai_utils import generate_description
from .notifications.webhook import notify_webhook



@receiver(post_save, sender=Post)
def generate_post_description(sender, instance, created, **kwargs):
    if created and not instance.description:
        instance.description = generate_description(instance.title)
        instance.save()

@receiver(post_save, sender=Post)
def handle_post_workflow(sender, instance, created, **kwargs):
    if created:
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

@receiver(post_save, sender=Comment)
def notify_post_author(sender, instance, created, **kwargs):
    if not created:
        return

    post = instance.post
    author = post.author
    email = getattr(author, 'email', None)

    if email:
        subject = f"Новый комментарий к вашему посту: {post.title} "
        message = f"{instance.author.username} написал:\n\n{instance.content}"
        send_mail(
            subject=subject,
            message=message,
            from_email='no-reply@genjiblog.local',
            recipient_list=[email],
        )
        payload = {
            "event": "new_comment",
            "post_title": post.title,
            "comment_author": instance.author.username,
            "content": instance.content,
        }
        notify_webhook(payload, settings.WEBHOOK_URL)