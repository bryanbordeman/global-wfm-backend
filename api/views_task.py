from rest_framework import generics, permissions
from .serializers_task import TaskSerializer, TaskListSerializer, TaskCreateSerializer
from task.models import Task as TaskModel
from task.models import TaskList as TaskListModel
from django.forms.models import model_to_dict
from django.http import JsonResponse

class TaskAssignee(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        assignee = self.kwargs['assignee']
        return TaskModel.objects.filter(**{"assignee_id" : assignee}).filter(is_deleted=False).order_by('due')

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

class TaskList(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskListSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskListModel.objects.all()