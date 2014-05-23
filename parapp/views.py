# -*- coding: utf-8 -*-
from django.db import models
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from parapp.models import Project, Calculation, Estimation, Analysis, Problem, Algorithm, Indicator
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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
    data['calculations'] = Calculation.objects.filter(project=project)
    data['analyzes']     = Analysis.objects.filter(project=project)
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
    data['project']    = project
    data['indicators'] = Indicator.objects.all()

    if request.method == 'GET':
        return TemplateResponse(request, 'estimation_create.html', {'errors': errors, 'data': data})

    name           = request.POST.get('name', 0)
    indicator_id   = request.POST.get('indicator', 0)
    indicator_type = request.POST.get('type', 0)
    input_data1    = request.FILES.get('input_data1', 0)
    input_data2    = request.FILES.get('input_data2', 0)

    if not name:
        errors['name'] = 'Имя оценки не введено'
    elif not input_data1:
        errors['input_data1'] = 'Входной файл не загружен'
    elif indicator_type == '2' and not input_data2:
        errors['input_data2'] = 'Входной файл не загружен'

    if not indicator_id:
        errors['indicator'] = 'Метод оценки не выбран'
    else:
        indicator = get_object_or_404(Indicator, pk=indicator_id)

    if errors.keys():
        data['name'] = name
        data['type'] = indicator_type
        return TemplateResponse(request, 'estimation_create.html', {'errors': errors, 'data': data})

    files_data = {}
    input_data1.seek(0)
    files_data["file1"] = input_data1.read()
    if indicator_type == '2':
        input_data2.seek(0)
        files_data["file2"]  = input_data2.read()
    input_data = json.dumps(files_data)
    new_est = Estimation(name=name, time='0', project=project, indicator=indicator,
        status='wait', input_data=input_data, output_data='')
    new_est.save()
    start_request(request.user, new_est.id, Estimation)
    return redirect('/estimation/' + str(new_est.id) + '/')

@login_required
def get_estimation(request, estimation_id):
    data, errors = {}, {}
    estimation = get_object_or_404(Estimation, pk=estimation_id)
    project    = get_object_or_404(Project, pk=estimation.project_id, user=request.user)
    data['estimation'] = estimation
    if request.is_ajax():
        return TemplateResponse(request, 'inc/estimation.html', {'errors': errors, 'data': data})
    return TemplateResponse(request, 'estimation.html', {'errors': errors, 'data': data})

@login_required
def create_calculation(request, project_id):
    data, errors = {}, {}

    project = get_object_or_404(Project, user=request.user, pk=project_id)
    data['project']    = project
    data['problems']   = Problem.objects.all()
    data['algorithms'] = Algorithm.objects.all()

    if request.method == 'GET':
        return TemplateResponse(request, 'calculation_create.html',
            {'errors': errors, 'data': data})

    name         = request.POST.get('name', 0)
    problem_id   = request.POST.get('problem_id', 0)
    algorithm_id = request.POST.get('algorithm_id', 0)

    if not name:
        errors['name'] = 'Имя оценки не введено'

    if not problem_id:
        errors['problem_id'] = 'Тестовая задача не выбрана'
    else:
        problem = get_object_or_404(Problem, pk=problem_id)

    if not algorithm_id:
        errors['algorithm_id'] = 'Алгоритм не выбран'
    else:
        algorithm = get_object_or_404(Algorithm, pk=algorithm_id)

    if errors.keys():
        data['name'] = name
        return TemplateResponse(request, 'calculation_create.html',
            {'errors': errors, 'data': data})

    new_calc = Calculation(name=name, time='0', project=project, problem=problem,
        algorithm=algorithm, status='wait', input_data='', output_data='')
    new_calc.save()
    start_request(request.user, new_calc.id, Calculation)
    return redirect('/calculation/' + str(new_calc.id) + '/')

@login_required
def get_calculation(request, calculation_id):
    data, errors = {}, {}
    calculation = get_object_or_404(Calculation, pk=calculation_id)
    project     = get_object_or_404(Project, pk=calculation.project_id, user=request.user)
    data['calculation'] = calculation
    data['algorithm']   = get_object_or_404(Algorithm, pk=calculation.algorithm.id)
    data['problem']     = get_object_or_404(Problem,   pk=calculation.problem.id)
    if request.is_ajax():
        return TemplateResponse(request, 'inc/calculation.html', {'errors': errors, 'data': data})
    return TemplateResponse(request, 'calculation.html', {'errors': errors, 'data': data})

def api_req(params, cookies):
    url  = 'http://127.0.0.1:8888/api/'
    try:
        resp = requests.post(url, data=params, cookies=cookies)
    except (requests.exceptions.RequestException) as e:
        return False
    sys.stderr.write(str(resp.status_code))
    sys.stderr.write(resp.text)
    if resp.status_code != 200:
        return False
    return json.loads(resp.text)

@csrf_exempt
def api_back(request):
    data, errors = {}, {}
    e_id   = request.POST.get('id',     0)
    data   = request.POST.get('data',   '')
    type   = request.POST.get('type',   '')
    status = request.POST.get('status', 'fail')
    time   = request.POST.get('time',   0)

    if type == "estimation":
        entity = get_object_or_404(Estimation, pk=e_id)
    elif type == "calculation":
        entity = get_object_or_404(Calculation, pk=e_id)
    elif type == "analysis":
        entity = get_object_or_404(Analysis, pk=e_id)
    else:
        return HttpResponse(json.dumps({'status': 'fail'}), content_type="application/json")

    entity.status      = status
    entity.output_data = data
    entity.time        = time
    entity.save()
    return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")

@csrf_exempt
def stub(request):
    return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")

@login_required
def get_analysis(request, calculation_id):
    data, errors = {}, {}
    calculation = get_object_or_404(Analysis, pk=calculation_id)
    project     = get_object_or_404(Project, pk=calculation.project_id, user=request.user)
    data['analysis']  = calculation
    data['algorithm'] = get_object_or_404(Algorithm, pk=calculation.algorithm.id)
    data['problem']   = get_object_or_404(Problem,   pk=calculation.problem.id)
    if request.is_ajax():
        return TemplateResponse(request, 'inc/analysis.html', {'errors': errors, 'data': data})
    return TemplateResponse(request, 'analysis.html', {'errors': errors, 'data': data})

@login_required
def create_analysis(request, calculation_id):
    pass

@login_required
def delete_entity(request, id, entity):
    ent     = get_object_or_404(entity, pk=id)
    project = get_object_or_404(Project, user=request.user, pk=ent.project_id)
    ent.delete()
    return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")

@login_required
def start_entity(request, id, entity):
    if start_request(request.user, id, entity):
        return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")
    return HttpResponse(json.dumps({'status': 'fail'}), content_type="application/json")

def start_request(user, id, entity):
    ent     = get_object_or_404(entity, pk=id)
    project = get_object_or_404(Project, user=user, pk=ent.project_id)
    type = entity.__name__.lower()
    params = {'type': type, 'id': id }
    if type == "calculation":
        algorithm = get_object_or_404(Algorithm, pk=ent.algorithm_id)
        problem   = get_object_or_404(Problem, pk=ent.problem_id)
        params['name_algorithm'] = algorithm.value
        params['name_problem']   = problem.value
    elif type == "calculation":
        indicator = get_object_or_404(Indicator, pk=ent.indicator_id)
        params['data'] = ent.input_data
        params['name'] = indicator.value
    api_response = api_req(params, {})
    if api_response and api_response['status'] == 'ok':
        ent.status = 'proc'
        ent.save()
        return True
    return
