from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user  = models.ForeignKey(User)
    name  = models.CharField(max_length=255)
    date_added    = models.DateTimeField(auto_now_add=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    descr = models.TextField()
    def __unicode__(self):
        return self.name or u''

class Problem(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    is_binary = models.BooleanField()
    def __unicode__(self):
        return self.name or u''

class Algorithm(models.Model):
    name = models.CharField(max_length=255)
    path = models.FilePathField(path=None, max_length=255)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __unicode__(self):
        return self.name or u''

class Calculation(models.Model):
    project     = models.ForeignKey(Project)
    algorithm   = models.ForeignKey(Algorithm)
    name        = models.CharField(max_length=255)
    time        = models.IntegerField(default=0)
    date        = models.DateTimeField(auto_now_add=True, blank=True)
    input_data  = models.TextField()
    output_data = models.TextField()
    def __unicode__(self):
        return self.name or u''

class Estimation(models.Model):
    STATUS = (
        ('wait', 'waiting'),
        ('prog', 'in progress'),
        ('ok',   'ok'),
        ('fail', 'fail'),
    )
    project     = models.ForeignKey(Project)
    problem     = models.ForeignKey(Problem)
    calc_1      = models.ForeignKey(Calculation, null=True, related_name='calc_1')
    calc_2      = models.ForeignKey(Calculation, null=True, related_name='calc_2')
    name        = models.CharField(max_length=255)
    status      = models.CharField(max_length=4, choices=STATUS, default='data')
    time        = models.IntegerField(default=0)
    date        = models.DateTimeField(auto_now_add=True, blank=True)
    input_data  = models.TextField()
    output_data = models.TextField()
    def __unicode__(self):
        return self.name or u''
