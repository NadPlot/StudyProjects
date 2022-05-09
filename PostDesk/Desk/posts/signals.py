from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Respond, Post
from django.template.loader import render_to_string
from django.conf import settings


# При отправке отклика пользователь должен получить e-mail с оповещением о нём
@receiver(post_save, sender=Respond)
def new_respond_notification(sender, instance, **kwargs):
    post = Post.objects.get(id=instance.post_id)
    if instance.status == 1:
        email = [instance.user.email]
        subject = 'PostDesk. Отклик принят'
        html_content = render_to_string(
            'taken_respond.html',
            {
                'user': instance.user,
                'post': post,
                'site_url': settings.SITE_URL,

            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email='margorit-k@yandex.ru',
            to=email,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        email = [post.user.email]
        subject = 'PostDesk. Отклик на ваш пост'
        html_content = render_to_string(
            'new_respond.html',
            {
                'user': post.user,
                'post': post,
                'site_url': settings.SITE_URL,

            }
        )
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email='margorit-k@yandex.ru',
            to=email,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()