# -*- coding: utf-8 -*-
from django.db import models
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from parapp.models import Project, Calculation, Estimation, Problem, Algorithm
from django.shortcuts import redirect, get_object_or_404

import os, sys
import datetime
import json
import requests

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
    user = authenticate(username=name, password=pass1)
    if user.is_active:
        auth_login(request, user)
        return redirect("/projects/")
    else:
        return HttpResponse("<html><body>Everything is BAD</body></html>")

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
                errors['data'] = u'Неверный логин или пароль'
        else:
            errors['data'] = u'Неверный логин или пароль'

    data['username']=username
    
    if errors.keys():
        return TemplateResponse(request, 'login.html', {'errors': errors, 'data': data})
    else:
        return redirect('/projects/')

def logout(request):
    auth_logout(request)
    return TemplateResponse(request, "logout.html")

@login_required
def create_project(request):
    response_data = {'status': 'fail'}
    name = request.POST.get('name', 0)
    if name:
        project = Project(
            name  = name,
            user  = request.user,
            descr =request.POST.get('descr', 0)
        )
        if project:
            response_data['status'] = 'ok'
            project.save()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def edit_project(request, project_id):
    result  = {'status': 'fail'}
    project = get_object_or_404(Project, user=request.user, pk=project_id)
    name    = request.POST.get('name')
    if name:
        project.name  = request.POST.get('name', 0)
        project.descr = request.POST.get('descr', 0)
        project.save()
        result['status'] = 'ok'
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def get_project(request, project_id):
    data, errors = {}, {}
    project = get_object_or_404(Project, user=request.user, pk=project_id)
    data['project']      = project
    data['estimations']  = Estimation.objects.filter(project=project)
    return TemplateResponse(request, 'project.html', {'errors': errors, 'data': data})

per_page = 20
@login_required
def list_project(request):
    all_projects, errors, data, num_projects = {}, {}, {}, {}
    data['projects'] = Project.objects.filter(
        user=request.user).order_by("-date_added")[:per_page]
    data['total'] = Project.objects.filter(user=request.user).count()
    data['offset'] = 0
    return TemplateResponse(request,'projects.html', {'errors': errors, 'data': data })

@login_required
def list_project_row(request):
    all_projects, errors, data, num_projects = {}, {}, {}, {}
    page = int(request.GET.get('page', 1))
    data['offset']   = (page - 1) * per_page
    data['projects'] = Project.objects.filter(
        user=request.user).order_by("-date_added")[data['offset']:data['offset'] + per_page]
    return TemplateResponse(request,'inc/project_list.html', {'errors': errors, 'data': data })


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, user=request.user, pk=project_id)
    project.delete()
    return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")

@login_required
def search_project(request):
    data, errors,  = {}, {}
    query = request.POST.get('q', 0)
    data['offset']   = 0
    data['projects'] = Project.objects.filter(
        user=request.user, name__icontains=query).order_by("-date_added")
    return TemplateResponse(request, 'inc/project_list.html', {'errors': errors, 'data': data })

@login_required
def create_estimation(request, project_id):
    data, errors = {}, {}

    project = get_object_or_404(Project, user=request.user, pk=project_id)
    data['problems'] = Problem.objects.all()

    if request.method == 'GET':
        return TemplateResponse(request, 'estimation_create.html', {'errors': errors, 'data': data})

    name         = request.POST.get('name', 0)
    problem_id   = request.POST.get('problem', 0)
    problem_type = request.POST.get('type', 0)
    input_data1  = request.FILES.get('input_data1', 0)
    input_data2  = request.FILES.get('input_data2', 0)

    if not name:
        errors['name'] = 'Имя оценки не введено'
    elif not input_data1:
        errors['input_data1'] = 'Входной файл не загружен'
    elif not input_data2:
        errors['input_data2'] = 'Входной файл не загружен'

    if not problem_id:
        errors['problem'] = 'Метод оценки не выбран'
    else:
        problem = get_object_or_404(Problem, pk=problem_id)

    if errors.keys():
        data['name'] = name
        data['type'] = problem_type
        return TemplateResponse(request, 'estimation_create.html', {'errors': errors, 'data': data})

    input_data1.seek(0)
    input_data2.seek(0)
    data1 = input_data1.read()
    data2 = input_data2.read()
    input_data = json.dumps({'file1': data1, 'file2': data2})
    new_est = Estimation(name=name, time='0', project=project, problem=problem,
        status='wait', input_data=input_data, output_data='')
    api_response = api_req({'id': new_est.id, 'file1': data1, 'file2': data2,
        'csrfmiddlewaretoken': request.COOKIES['csrftoken']}, {'csrftoken': request.COOKIES['csrftoken']})
    # send to calc server
    if api_response and api_response['status'] == 'ok':
        new_est.status = 'proc'
    new_est.save()
    return redirect('/estimation/' + str(new_est.id) + '/')

@login_required
def get_estimation(request, estimation_id):
    data, errors = {}, {}
    estimation = get_object_or_404(Estimation, pk=estimation_id)
    project    = get_object_or_404(Project, pk=estimation.project_id, user=request.user)
    data['estimation'] = estimation
    return TemplateResponse(request, 'estimation.html', {'errors': errors, 'data': data})

def api_req(params, cookies):
    url  = 'http://127.0.0.1:8000/new_calc/'
    try:
        resp = requests.get(url, data=params, cookies=cookies)
    except (requests.exceptions.RequestException) as e:
        return False
    if resp.status_code != 200:
        return False
    sys.stderr.write(resp.text)
    return json.loads(resp.text)

def api_back(request):
    data, errors = {}, {}
    e_id   = request.GET.get('id',     0)
    data   = request.GET.get('data',   '')
    status = request.GET.get('status', 'fail')
    time   = request.GET.get('time',   0)

    estimation = get_object_or_404(Estimation, pk=e_id)
    estimation.status      = status
    estimation.output_data = data
    estimation.time        = time
    estimation.save()
    return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")

def stub(request):
    return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")
