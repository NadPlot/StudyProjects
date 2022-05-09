from django.forms import ModelForm, DateInput
from django_summernote.widgets import SummernoteWidget
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        widgets = {
            'content': SummernoteWidget(),
        }
        fields = ['title', 'content', 'user', 'category']
        labels = {
            'title': ('Заголовок'),
            'content': (''),
            'user': ('Пользователь'),
            'category': ('Категория'),
        }


class Date(DateInput):
    input_type = 'date'