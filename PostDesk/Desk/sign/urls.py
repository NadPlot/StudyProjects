from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import EnterCodeView, create_code

urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('code/', create_code, name='code'),
    path('code/confirm', EnterCodeView.as_view(), name='enter_code',)
]