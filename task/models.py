from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from django.contrib import admin

class TaskList(models.Model):
    title = models.CharField(max_length=100)
    show_completed = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    title = models.CharField(max_length=100)
    notes = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(1000)])
    due = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    completed = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    notes = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(1000)])
    due = models.DateField(null=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    subtasks = models.ManyToManyField(SubTask, blank=True)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    completed = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.project} | {self.title}'
