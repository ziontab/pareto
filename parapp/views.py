# -*- coding: utf-8 -*-
from django.db import models
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from parapp.models import Project, Calculation, Estimation, Problem, Algorithm
from django.shortcuts import redirect

import subprocess
import os
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
                errors['data'] = u'Не верный логин или пароль'
        else:
            errors['data'] = u'Не верный логин или пароль'

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
    name = request.POST.get('proj_name',0)
    descript = request.POST.get('descr',0)
    if not name:
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    project = Project(name = name, user = request.user)
    if project:
        response_data['status'] = 'ok'
        project.save()
    return redirect('/projects/')

@login_required
def edit_project(request, project_id):
    data = {}
    try:
        data['project'] = Project.objects.get(user=request.user, pk=project_id)
    except Project.DoesNotExist:
        raise Http404
    if request.method == 'GET':
        return TemplateResponse(request,'editproject.html',{'data': data})
    else:
        name = request.POST.get('new_name',0)
        description = request.POST.get('new_descr',0)
        Project.objects.filter(id=project_id).update(name=name)
        return redirect('/projects/')

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
    all_projects, errors, data, num_projects = {}, {}, {}, {}
    #num_paginator = Projects.objects.filter(user=request.user).count()
    all_projects = Project.objects.filter(user=request.user).order_by("-date")

    paginator = Paginator(all_projects, 8)
    page = request.GET.get('page')

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return TemplateResponse(request,'projects.html',
        {'errors': errors, 'data': data, 'num_pages':xrange(1,paginator.num_pages+1)})


@login_required
def delete_project(request, project_id):
    try:
        project = Project.objects.get(user=request.user, pk=project_id)
    except Project.DoesNotExist:
        raise Http404
    project.delete()
    return redirect('/projects/')

@login_required
def search_project(request):
    if request.method == 'GET':
        return redirect('/projects/')
    else:
        data, errors,  = {}, {}
        query = request.POST.get('search_q',0)
        data = Project.objects.filter(user=request.user,name__icontains=query).order_by("-date")
        return TemplateResponse(request, 'search_projects.html', {'errors': errors, 'data': data, 'query':query})


@login_required
def create_calculation(request, project_id):
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
def create_estimation(request, project_id):
    data, errors = {}, {}
    try:
        project = Project.objects.get(user=request.user, pk=project_id)
    except Project.DoesNotExist:
        raise Http404
    data['project']      = project
    data['problems']     = Problem.objects.all()
    data['estimations']  = Estimation.objects.filter(project=project)
    data['calculations'] = Calculation.objects.filter(project=project)

    if request.method == 'GET':
        return TemplateResponse(request, 'estimation_create.html', {'errors': errors, 'data': data})

    name         = request.POST.get('name', 0)
    problem_id   = request.POST.get('problem', 0)
    calc_1       = request.POST.get('calc_1', 0)
    calc_2       = request.POST.get('calc_2', 0)
    problem_type = request.POST.get('type', 0)
    input_type   = request.POST.get('input_type', 0)
    input_data1  = request.FILES.get('input_data1', 0)
    input_data2  = request.FILES.get('input_data2', 0)

    if not name:
        errors['name'] = 'Имя оценки не введено'
    if not input_type:
        errors['input_type'] = 'Типа входных данных не определен'
    elif (input_type == '1') and not input_data1:
        errors['input_data1'] = 'Входной файл не загружен'
    elif (input_type == '1') and not input_data2:
        errors['input_data2'] = 'Входной файл не загружен'
    elif (input_type == '2') and not (calc_1 and calc_2):
        errors['calc_1'] = 'Расчеты не выбранны'
    if not problem_id:
        errors['problem'] = 'Метод оценки не выбран'
    else:
        try:
            problem = Problem.objects.get(pk=problem_id)
        except Problem.DoesNotExist:
            raise Http404

    if errors.keys():
        data['name']       = name
        data['type']       = problem_type
        data['input_type'] = input_type
        return TemplateResponse(request, 'estimation_create.html', {'errors': errors, 'data': data})

    if (input_type == '1'):
        result = handle_execution(problem.path, input_data1, input_data2)
        input_data1.seek(0)
        input_data2.seek(0)
        new_est = Estimation(name=name,
            input_data=input_data1.read() + "//////\n" + input_data2.read(),
            output_data=result, time='10', project=data['project'],problem=problem)
        new_est.save()
        return redirect('/estimation/' + str(new_est.id) + '/')
    return HttpResponse("<html><body>calculations not handled</body></html>")


def handle_execution(path, file_data1, file_data2):
    tmp_file_name_1 = '/tmp/buff1.txt'
    tmp_file_name_2 = '/tmp/buff2.txt'
    for file_struct in [ [tmp_file_name_1, file_data1], [tmp_file_name_2, file_data2]]:
        destination = open(file_struct[0], 'wb')
        for chunk in file_struct[1].chunks():
            destination.write(chunk)
        destination.close()

    args = (path, tmp_file_name_1, tmp_file_name_2 , "2", "4")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output

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
