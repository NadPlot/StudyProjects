
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, View, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Respond
from .forms import PostForm
from .filters import RespondFilter


# Лента новостей, все объявления
class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-add_time')


# Добавить объявление (создание)
class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    template_name = 'post_add.html'
    form_class = PostForm


# Редактировать объявление
class UpdatePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('posts.change_post',)
    template_name = 'post_add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# Лента откликов, все отклики
class RespondList(PermissionRequiredMixin, ListView):
    permission_required = ('posts.view_respond', )
    model = Respond
    template_name = 'responds.html'
    context_object_name = 'respond'
    queryset = Respond.objects.order_by('-add_time')

    def qet_filter(self):
        return RespondFilter(self.request.GET, queryset=super(RespondList).get_queryset())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RespondFilter(self.request.GET, queryset=self.get_queryset(), request=self.request)
        return context


# Добавить отклик
class RespondAdd(PermissionRequiredMixin, View):
    permission_required = ('posts.add_respond',)

    def get(self, request, id):
        post = Post.objects.filter(id=id)

        context = {
            'posts': post
        }
        return render(request, 'respond_add.html', context)

    def post(self, request, *args, **kwargs):
        respond = Respond(
            text=request.POST['text'],
            user=request.user,
            post_id=request.POST['post_id'],
            status=request.POST['status'],
        )
        respond.save()
        return redirect('/posts')


# удаление отклика
class RespondDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('posts.delete_respond',)
    template_name = 'respond_delete.html'
    queryset = Respond.objects.all()
    success_url = '/posts/responds/'


# принять отклик
@login_required
def respond_take(request, id):
    respond = Respond.objects.get(id=id)
    respond.take_respond()
    return redirect('/posts/responds/')

