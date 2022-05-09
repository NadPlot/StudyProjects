from random import randrange as rnd
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, View
from .models import BaseRegisterForm, ConfirmCode


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/sign/code/'


# Промежуточный, для создания одноразового кода
def create_code(request):
    user = request.user
    ConfirmCode.objects.create(user=user, code=rnd(1000, 9999, 1))
    return redirect('/sign/code/confirm')


class EnterCodeView(View):

    def get(self, request):
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'sign/enter_code.html', context)

    def post(self, request):
        user = request.user
        registred_group = Group.objects.get(name='Registred')
        enter_code = int(request.POST['code'])
        code = ConfirmCode.objects.get(user=user)
        if code.code == enter_code:
            registred_group.user_set.add(user)
            code.delete()
            return redirect('/posts')
        else:
            code.delete()
            return render(request, 'sign/wrang_code.html')