from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    date = models.DateTimeField('date started')

class Problem(models.Model):
    name = models.CharField(max_length=255)
    path = models.FilePathField(path=None, max_length=255)
    date = models.DateTimeField('date published')
    is_binary = models.BooleanField()

class Algorithm(models.Model):
    name = models.CharField(max_length=255)
    path = models.FilePathField(path=None, max_length=255)
    date = models.DateTimeField('date published')

class Calculation(models.Model):
    project     = models.ForeignKey(Project)
    algorithm   = models.ForeignKey(Algorithm)
    name        = models.CharField(max_length=255)
    time        = models.IntegerField(default=0)
    date        = models.DateTimeField('date executed')
    input_data  = models.TextField()
    output_data = models.TextField()

class Estimation(models.Model):
    project     = models.ForeignKey(Project)
    problem     = models.ForeignKey(Problem)
    calculation = models.ForeignKey(Calculation)
    calculation = models.ForeignKey(Calculation)
    name        = models.CharField(max_length=255)
    time        = models.IntegerField(default=0)
    date        = models.DateTimeField('date executed')
    input_data  = models.TextField()
    output_data = models.TextField()
