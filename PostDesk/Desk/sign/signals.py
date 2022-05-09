from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import ConfirmCode


# Отправка кода регистрации на почту
@receiver(post_save, sender=ConfirmCode)
def send_code(sender, instance, **kwargs):
    email = [instance.user.email]
    subject = 'PostDesk. Код подтверждения регистрации'
    html_content = render_to_string(
        'sign/send_code.html',
        {
            'user': instance.user.username,
            'code': instance.code,
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