from django.contrib import admin
from .models import TaskList, SubTask, Task

admin.site.register(TaskList)
admin.site.register(SubTask)
admin.site.register(Task)