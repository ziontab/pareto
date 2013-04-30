# -*- coding: utf-8 -*-
from django.db import models
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from parapp.models import Project, Calculation, Estimation
from django.shortcuts import redirect

import datetime
import json

@login_required
def get_main(request):
    return redirect('/projects/')

def register(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'register.html')

    data, errors = {}, {}
    name  = request.POST.get('username',  0)
    email = request.POST.get('email',     0)
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
    return redirect('/projects/')

def login(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'login.html')

    data, errors = {}, {}
    username = request.POST.get('username', 0)
    password = request.POST.get('password', 0)
    user     = None

    if not username:
        errors['username'] = u'Логин не введен'
    elif not password:
        errors['password'] = u'Пароль не введен'
    else:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
            else:
                errors['data'] = u'Не верный логин или пароль'
        else:
            errors['data'] = u'Не верный логин или пароль'

    if errors.keys():
        return TemplateResponse(request, 'login.html', {'errors': errors, 'data': data})
    else:
        return redirect('/projects/')

@login_required
def create_project(request):
    response_data = {'status': 'fail'}
    name = request.GET.get('name', 0)
    if not name:
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    project = Project(name = name, user = request.user)
    if project:
        response_data['status'] = 'ok'
        project.save()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def get_project(request, project_id):
    data, errors = {}, {}
    try:
        project = Project.objects.get(user=request.user, pk=project_id)
    except Project.DoesNotExist:
        raise Http404
    data['project']      = project
    data['estimations']  = Estimation.objects.filter(project=project)
    data['calculations'] = Calculation.objects.filter(project=project)
    return TemplateResponse(request, 'project.html', {'errors': errors, 'data': data})

@login_required
def list_project(request):
    data, errors = {}, {}
    data['projects'] = Project.objects.filter(user=request.user)
    return TemplateResponse(request, 'projects.html', {'errors': errors, 'data': data})

@login_required
def create_calculation(request):
    html = "<html><body>create_calculation</body></html>"
    return HttpResponse(html)

@login_required
def get_calculation(request, calculation_id):
    data, errors = {}, {}
    try:
        calculation = Calculation.objects.get(pk=calculation_id)
        project     = Project.objects.get(pk=calculation.project_id, user=request.user)
    except Calculation.DoesNotExist:
        raise Http404
    except Project.DoesNotExist:
        raise Http404
    data['calculation'] = calculation
    return TemplateResponse(request, 'calculation.html', {'errors': errors, 'data': data})

@login_required
def create_estimation(request):
    html = "<html><body>no create_estimation</body></html>"
    return HttpResponse(html)

@login_required
def get_estimation(request, estimation_id):
    data, errors = {}, {}
    try:
        estimation = Estimation.objects.get(pk=estimation_id)
        project     = Project.objects.get(pk=estimation.project_id, user=request.user)
    except Estimation.DoesNotExist:
        raise Http404
    except Project.DoesNotExist:
        raise Http404
    data['estimation'] = estimation
    return TemplateResponse(request, 'estimation.html', {'errors': errors, 'data': data})
