from rest_framework import generics, permissions
from .serializers_task import TaskSerializer
from task.models import Task as TaskModel

class Task(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TaskModel.objects.filter(is_deleted=False).filter(assignee=user).order_by('-created')



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
