from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from .forms import Date



class PostFilter(FilterSet):
    add_time = DateFilter(field_name='add_time', lookup_expr='gte', label='Позже даты', widget=Date)
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Пользователь')


    class Meta:
        model = Post
        fields = {

        }