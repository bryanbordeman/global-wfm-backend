from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone

class TaskList(models.Model):
    title = models.CharField(max_length=100)
    show_completed = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    title = models.CharField(max_length=100)
    notes = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(1000)])
    # due = models.DateField(null=True)
    # created = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    # is_deleted = models.BooleanField(default=False)
    completed = models.DateTimeField(auto_now_add=True, editable=True)
    updated = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.is_complete == True:
            self.completed = timezone.now()
        # else:
        #     self.completed = ''
        # if not self.id:
        #     self.created = timezone.now()
        self.updated = timezone.now()
        return super(SubTask, self).save(*args, **kwargs)

class Task(models.Model):
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    # assignee = models.ForeignKey(User, related_name='related_assignee', on_delete=models.CASCADE)
    
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    notes = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(1000)])
    due = models.DateField(null=True)
    subtasks = models.ManyToManyField(SubTask, blank=True)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    completed = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.project} | {self.title}'
