from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from celery import shared_task
from .models import Post, Category, Subscribes


@shared_task
def send_email_subscribes(oid):
    post = Post.objects.get(pk=oid)
    categoryes = Category.objects.filter(post=post)
    subject = f'{post.title}'
    for category in categoryes:
        subscribes = Subscribes.objects.filter(
            subscribe=category)  #получаем подписчиков на категорию
        for subscriber in subscribes:
            email = []
            email.append(subscriber.user.email)
            username = subscriber.user.username

            html_content = render_to_string(
                'send_new_post.html',
                {
                    'post': post,
                    'username': username,
                    'category': category.name,
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
            return print('Send email')


@shared_task
def weekly_send_email():
    subject = f'Новости за неделю'
    date = make_aware(datetime.today() - timedelta(days=11))
    categoryes = Category.objects.all()
    for category in categoryes:
        post = Post.objects.filter(add_time__gte=date.isoformat(),
                                   post_cat=category)
        subscribes = Subscribes.objects.filter(
            subscribe=category)
        for subscriber in subscribes:
            email = []
            email.append(subscriber.user.email)
            username = subscriber.user.username

            html_content = render_to_string(
                'weekly_send.html',
                {
                    'post': post,
                    'username': username,
                    'category': category.name,
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