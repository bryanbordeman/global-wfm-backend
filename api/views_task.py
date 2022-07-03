from rest_framework import generics, permissions
from .serializers_task import TaskSerializer, TaskListSerializer
from task.models import Task as TaskModel
from task.models import TaskList as TaskListModel

class Task(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tasklist = self.kwargs['tasklist']
        assignee = self.kwargs['assignee']
        # user = self.request.user
        # return TaskModel.objects.filter(is_deleted=False).filter(assignee=user).order_by('-created')
        return TaskModel.objects.filter(**{"assignee_id" : assignee}).filter(is_deleted=False).filter(tasklist=tasklist).order_by('-created')
        # return TaskModel.objects.filter(is_deleted=False).order_by('-created')[:2]

# class TaskCreate(generics.ListCreateAPIView):
#     serializer_class = TaskSerializer
#     permissions_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return TaskModel.objects.all()
    
#     def perform_create(self, serializer):
#         serializer.save()

# class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TaskSerializer
#     permissions_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return TaskModel.objects.all()

class TaskList(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskListSerializer
    permissions_classes = [permissions.IsAuthenticated]

    

    def get_queryset(self):
        return TaskListModel.objects.all()