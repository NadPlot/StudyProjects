from django.urls import path
from .views import PostsList, CategoryPostsList, PostDetail, SearchList, AddView, PostUpdateView, PostDeleteView
from django.contrib.auth.views import LogoutView
from .views import upgrade_me, subscribe_me


urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('category/<int:category_id>/', CategoryPostsList.as_view(), name='category_news'),
    path('subscribe/category/<int:category_id>/', subscribe_me, name='subscribe_category'),
    path('post/<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', SearchList.as_view(), name='search'),
    path('add/', AddView.as_view(), name='post_add'),
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('add/upgrade/', upgrade_me, name='upgrade'),
    path('<int:id>/subscribe', subscribe_me, name='subscribe'),
]
