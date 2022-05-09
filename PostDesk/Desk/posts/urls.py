from django.urls import path
from .views import PostsList, AddPost, RespondList, RespondAdd, RespondDeleteView, respond_take, UpdatePost


urlpatterns = [
    path('', PostsList.as_view(), name='all_posts'), # Лента объявлений
    path('my/', PostsList.as_view(template_name='posts_user.html'), name='posts_user'),  # Лента объявления пользователя
    path('add/', AddPost.as_view(), name='add_post'), # Добавить (создать) объявление
    path('edit/<int:pk>', UpdatePost.as_view(), name='post_update'), # редактировать объявление
    path('responds/', RespondList.as_view(), name='responds'), # Лента все отклики на объявления пользователя
    path('add/respond/<int:id>', RespondAdd.as_view(), name='add_respond'), # Добавить отклик на конкретное объявление
    path('respond/<int:pk>/delete', RespondDeleteView.as_view(), name='delete_respond'), # Удалить отклик
    path('respond/<int:id>/take', respond_take, name='take_respond'), # Принять отклик

]