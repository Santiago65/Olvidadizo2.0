from django.contrib import admin
from .models import Task, Cumple,SharedTask



class TaskAdmin(admin.ModelAdmin):
    readonly_fields =("created",)
# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Cumple)
admin.site.register(SharedTask)


