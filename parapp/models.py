from django.db import models
from django.contrib.auth.models import User

STATUS = (
    ('wait', 'waiting'),
    ('prog', 'in progress'),
    ('ok',   'ok'),
    ('fail', 'fail'),
)

class Project(models.Model):
    user  = models.ForeignKey(User)
    name  = models.CharField(max_length=255)
    date_added    = models.DateTimeField(auto_now_add=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    descr = models.TextField()
    def __unicode__(self):
        return self.name or u''

class Problem(models.Model):
    name      = models.CharField(max_length=255)
    value     = models.CharField(max_length=255)
    date      = models.DateTimeField(auto_now_add=True, blank=True)
    def __unicode__(self):
        return self.name or u''

class Algorithm(models.Model):
    name  = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    date  = models.DateTimeField(auto_now_add=True, blank=True)
    def __unicode__(self):
        return self.name or u''

class Indicator(models.Model):
    name  = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    date  = models.DateTimeField(auto_now_add=True, blank=True)
    is_binary = models.BooleanField()
    def __unicode__(self):
        return self.name or u''

class Calculation(models.Model):
    project     = models.ForeignKey(Project)
    name        = models.CharField(max_length=255)
    status      = models.CharField(max_length=4, choices=STATUS, default='wait')
    time        = models.IntegerField(default=0)
    date        = models.DateTimeField(auto_now=True, blank=True)
    input_data  = models.TextField()
    output_data = models.TextField()
    algorithm   = models.ForeignKey(Algorithm)
    problem     = models.ForeignKey(Problem)
    def __unicode__(self):
        return self.name or u''

class Estimation(models.Model):
    project     = models.ForeignKey(Project)
    name        = models.CharField(max_length=255)
    status      = models.CharField(max_length=4, choices=STATUS, default='wait')
    time        = models.IntegerField(default=0)
    date        = models.DateTimeField(auto_now=True, blank=True)
    input_data  = models.TextField()
    output_data = models.TextField()
    indicator   = models.ForeignKey(Indicator)
    def __unicode__(self):
        return self.name or u''

class Analysis(models.Model):
    project     = models.ForeignKey(Project)
    name        = models.CharField(max_length=255)
    status      = models.CharField(max_length=4, choices=STATUS, default='wait')
    time        = models.IntegerField(default=0)
    date        = models.DateTimeField(auto_now=True, blank=True)
    input_data  = models.TextField()
    output_data = models.TextField()
    problems    = models.TextField()
    algorithms  = models.TextField()
    def __unicode__(self):
        return self.name or u''
