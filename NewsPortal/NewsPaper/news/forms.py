from django.forms import ModelForm, DateInput
from .models import Post

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'post_or_news', 'text', 'author', 'post_cat']
        labels = {
            'title': ('Заголовок'),
            'post_or_news': ('Тип поста'),
            'text': ('Текст поста'),
            'author': ('Автор'),
            'post_cat': ('Категория'),
        }


class Date(DateInput):
    input_type = 'date'


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user