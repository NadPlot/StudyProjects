from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
import datetime
from django.utils.timezone import make_aware
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category, Subscribes, PostLimitException
from django.conf import settings


# Отправка уведомлений на почту при добавлении нового поста подписчикам на категорию
@receiver(m2m_changed, sender=Post.post_cat.through)
def notify_subscribes(sender, instance, **kwargs):
    subject = f'{instance.title}'
    post = Post(
        id=instance.id,
        title=instance.title,
        text=instance.text,
    )

    action = kwargs.pop('action', None)
    if action == 'post_add':
        # в зависимости от того, какая категория поста
        category = Category.objects.filter(post=instance)
        for id in category:
            subscribes = Subscribes.objects.filter(subscribe=id)  #получаем подписчиков на категорию
            for subscriber in subscribes:
                email = []
                email.append(subscriber.user.email)
                username = subscriber.user.username

                html_content = render_to_string(
                    'send_new_post.html',
                    {
                        'post': post,
                        'username': username,
                        'category': id.name,
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


#Ограничение количества публикаций:
@receiver(pre_save, sender=Post)
def post_limit(sender, instance, **kwargs):
    date = make_aware(datetime.datetime.today() - datetime.timedelta(hours=24))
    posts = Post.objects.filter(add_time__gte=date.isoformat(), author=instance.author)  # <QuerySet []>
    if len(posts) >= 3:
        raise PostLimitException(f"Пользователь не может публиковать более 3-х новостей в сутки") #not done