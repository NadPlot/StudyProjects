import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from news.models import Post, User, Category, Subscribes

from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.conf import settings

logger = logging.getLogger(__name__)


# задача по отправке писем 1 раз в неделю
def posts_week():
    subject = f'Новости за неделю'
    date = make_aware(datetime.today() - timedelta(days=7))
    categoryes = Category.objects.all() #<QuerySet [<Category: Недвижимость>, <Category: Спорт>, <Category: Авто>, <Category: Инвестиции>]>
    for category in categoryes:
        post = Post.objects.filter(add_time__gte=date.isoformat(), post_cat=category) #<QuerySet [<Post: Post object (..)>, <Post: Post object (..)>]>
        subscribes = Subscribes.objects.filter(subscribe=category) #<QuerySet [<Subscribes: Спорт>, <Subscribes: Спорт>]>
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
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand): #The base class from which all management commands ultimately derive.
    help = "Runs weekly." #A short description of the command,
    # which will be printed in the help message when the user runs the command python manage.py help <command>.

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            posts_week,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="posts_week",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'posts_week'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")