from django.urls import path
from . import views
from .views import PostsList, PostDetail, SearchList, AddView, PostUpdateView, PostDeleteView
from django.contrib.auth.views import LogoutView
from .views import upgrade_me, subscribe_me

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', SearchList.as_view()),
    path('add/', AddView.as_view()),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('add/upgrade/', upgrade_me, name='upgrade'),
    path('<int:id>/subscribe', subscribe_me, name='subscribe'),

]