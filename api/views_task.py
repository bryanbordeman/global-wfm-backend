from email.quoprimime import quote
from rest_framework import generics, permissions
from .serializers_task import TaskSerializer, TaskListSerializer, TaskCreateSerializer, SubTaskCompleteSerializer, SubTaskSerializer, TaskCompleteSerializer
from task.models import Task as TaskModel
from task.models import TaskList as TaskListModel
from task.models import SubTask as SubTaskModel
from django.utils.timezone import now

class TaskAssignee(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assignee = self.kwargs['assignee']
        return TaskModel.objects.filter(**{"assignee_id" : assignee}).filter(is_deleted=False).filter(is_complete=False).order_by('due')

class TaskProject(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = self.kwargs['project']
        return TaskModel.objects.filter(**{"project_id" : project}).filter(is_deleted=False).filter(is_complete=False).order_by('assignee')

class TaskService(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service = self.kwargs['service']
        return TaskModel.objects.filter(**{"service_id" : service}).filter(is_deleted=False).filter(is_complete=False).order_by('assignee')

class TaskHSE(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hse = self.kwargs['hse']
        return TaskModel.objects.filter(**{"hse_id" : hse}).filter(is_deleted=False).filter(is_complete=False).order_by('assignee')

class TaskQuote(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        quote = self.kwargs['quote']
        return TaskModel.objects.filter(**{"quote_id" : quote}).filter(is_deleted=False).filter(is_complete=False).order_by('assignee')

class TaskAssigneeCompleteList(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assignee = self.kwargs['assignee']
        tasklist = self.kwargs['tasklist']
        return TaskModel.objects.filter(**{"assignee_id" : assignee}).filter(**{"tasklist_id" : tasklist}).filter(is_deleted=False).filter(is_complete=True).order_by('due')[:100]

class TaskAssigneeList(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assignee = self.kwargs['assignee']
        tasklist = self.kwargs['tasklist']
        return TaskModel.objects.filter(**{"assignee_id" : assignee}).filter(**{"tasklist_id" : tasklist}).filter(is_deleted=False).filter(is_complete=False).order_by('due')

class TaskCreate(generics.ListCreateAPIView):
    serializer_class = TaskCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskModel.objects.all()

    def perform_update(self, serializer):
        serializer.instance.updated=(now())
        serializer.save()

class TaskList(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskListSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskListModel.objects.all()

class TaskToggleCompleted(generics.UpdateAPIView):
    '''Complete Subtask'''
    serializer_class = TaskCompleteSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskModel.objects.all()
    
    def perform_update(self, serializer):
        serializer.instance.is_complete=not(serializer.instance.is_complete)
        serializer.instance.completed=(now())
        serializer.save()

class SubtaskToggleCompleted(generics.UpdateAPIView):
    '''Complete Subtask'''
    serializer_class = SubTaskCompleteSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubTaskModel.objects.all()
    
    def perform_update(self, serializer):
        serializer.instance.is_complete=not(serializer.instance.is_complete)
        serializer.instance.completed=(now())
        serializer.save()

class SubtaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubTaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubTaskModel.objects.all()

class SubtaskCreate(generics.ListCreateAPIView):
    serializer_class = SubTaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubTaskModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
