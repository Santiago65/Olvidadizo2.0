from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    users = models.ManyToManyField(User, related_name='tasks')

class Cumple(models.Model): 
    users = models.ManyToManyField(User, related_name='cumples')
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255, default='Cumpleañero')

    def __str__(self):
        return self.descripcion
