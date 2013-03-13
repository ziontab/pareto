# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

import datetime

def register(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'register.html')

    errors = {}
    data   = {}
    name  = request.POST.get('username', 0)
    email = request.POST.get('email', 0)
    pass1 = request.POST.get('password1', 0)
    pass2 = request.POST.get('password2', 0)
    if name:
        data['name'] = name
    else:
        errors['name'] = u'Логин пользователя не введен'
    if email:
        data['email'] = email
    else:
        errors['email'] = u'Email пользователя не введен'

    if not pass1 or not pass2:
        errors['password'] = u'Пароль пользователя не введен'
    elif pass1 != pass2:
        errors['password'] = u'Введенный пароль не совпадает'

    if errors.keys():
        return TemplateResponse(request, 'register.html', {'errors': errors, 'data': data})

    user = User.objects.create_user(name, email, pass1)
    user.save()
    html = "<html><body>user</body></html>"
    return HttpResponse(html)

def login(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'login.html')

    username = request.POST.get('username', 0)
    password = request.POST.get('password', 0)

    if not username and not password:
        html = "<html><body>invalid data</body></html>"
        return HttpResponse(html)

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            html = "<html><body>active user</body></html>"
            return HttpResponse(html)

        else:
            html = "<html><body>disabled user</body></html>"
            return HttpResponse(html)
    else:
        html = "<html><body>no user such</body></html>"
        return HttpResponse(html)
