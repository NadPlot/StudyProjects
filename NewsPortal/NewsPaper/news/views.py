from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .filters import PostFilter
from .models import Post, Author, Subscribes, Category
from .forms import PostForm
from .tasks import send_email_subscribes


# Вывод всех новостей (лента)
class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-add_time')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(
            name='authors').exists()
        return context

# Поиск по новостям
class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = '-add_time'

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter']= PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


# Пост отдельно
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class AddView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'add.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save() #<Post: Post object (..)>
        send_email_subscribes.apply_async([post.pk], countdown=5)
        return redirect(f'/news/{post.pk}')


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# Удаление поста
class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


# Добавление в группу "Автор" по кнопке
@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/news')


# Кнопка подписаться на категорию поста
@login_required
def subscribe_me(request, id):
    user = request.user.id
    post_category = Category.objects.filter(post=id)
    for category in post_category:
        cat = category.name
        if Subscribes.objects.filter(user_id=user, subscribe=category).exists():
            continue
        else:
            Subscribes.objects.create(user_id=user, subscribe=category)
            return HttpResponse(f"Вы подписались на новости в категории {cat}")
    return HttpResponse(f"Вы уже подписаны на новости в категории {cat}")