from rest_framework import generics, permissions
from .serializers_task import TaskSerializer, TaskListSerializer, TaskCreateSerializer, SubTaskCompleteSerializer, SubTaskSerializer, TaskCompleteSerializer
from task.models import Task as TaskModel
from task.models import TaskList as TaskListModel
from task.models import SubTask as SubTaskModel
from django.utils.timezone import now
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import transaction
import boto3
from django.conf import settings

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
        return TaskModel.objects.filter(**{"assignee_id" : assignee}).filter(**{"tasklist_id" : tasklist}).filter(is_deleted=False).filter(is_complete=True).order_by('-due')[:50]

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
        serializer.instance.updated = now()
        serializer.save()

    def destroy_attachments(self, instance):
        """
        Delete attachments associated with the task instance.

        Args:
            instance: Task instance
        """
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        try:
            attachments = instance.attachments.all()

            for attachment in attachments:
                file_path = str(attachment.document)  
                s3.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=file_path
                )
                attachment.delete()

        except Exception as e:
            print("Exception:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    def perform_destroy(self, instance):
        """
        Perform destroy action and delete associated attachments.

        Args:
            instance: Task instance
        """
        try:
            with transaction.atomic():
                self.destroy_attachments(instance)
                instance.delete()

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'success': 'Task and attachments deleted successfully.'})

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

class TaskToggleRead(generics.UpdateAPIView):
    '''Mark Task as read'''
    serializer_class = TaskCompleteSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskModel.objects.all()

    def perform_update(self, serializer):
        serializer.instance.is_read=not(serializer.instance.is_read)
        serializer.save()

class TaskReadCount(generics.ListAPIView):
    '''Employee view'''
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        assignee = self.kwargs['assignee']
        count = TaskModel.objects.filter(assignee_id=assignee, is_read=False, is_complete=False).count()
        response_data = {'count': count}
        return Response(response_data)

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