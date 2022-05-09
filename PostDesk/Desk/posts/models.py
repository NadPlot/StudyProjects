from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    add_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def get_absolute_url(self):
        return f'/posts/'

    def __str__(self):
        return f'{self.title}'


class Respond(models.Model):
    add_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def take_respond(self):
        self.status = True
        self.save()

    def __str__(self):
        return f'{self.post}'