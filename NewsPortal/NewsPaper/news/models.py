from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your models here.

class Category (models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribes_user = models.ManyToManyField(User, through='Subscribes')

    def __str__(self):
        return f'{self.name}'


class Author (models.Model):
    user_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


    def update_rating(self, rating):
        self.user_rating = rating
        self.save()


class Post (models.Model):
    post = "PO"
    news = "NE"

    POSTS = [
        (post, "Статья"),
        (news, "Новость")
    ]

    post_or_news = models.CharField(max_length=2, choices=POSTS, default=post)
    add_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_cat = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name}'


class Comment (models.Model):
    text = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    post_rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class Subscribes(models.Model):
    class Meta:
        unique_together = (('user', 'subscribe'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribe = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subscribe}'


class PostLimitException(Exception):
    pass