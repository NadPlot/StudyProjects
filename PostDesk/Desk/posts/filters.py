from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Respond, Post, User
from .forms import Date


class RespondFilter(FilterSet):

    def user_posts(request):
        return Post.objects.filter(user=request.user)

    add_time = DateFilter(field_name='add_time', label='Дата', widget=Date)
    post = ModelChoiceFilter(queryset=user_posts, label='Пост')

    class Meta:
        model = Respond
        fields = []