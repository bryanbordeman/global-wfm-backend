from rest_framework import generics, permissions
from .serializers_report import ProjectReportSerializer, ProjectReportCreateSerializer
from .serializers_report import IncidentReportSerializer, IncidentReportCreateSerializer
from .serializers_report import DoorServiceReportSerializer, DoorServiceReportCreateSerializer
from report.models import ProjectReport as ProjectReportModel
from report.models import IncidentReport as IncidentReportModel
from report.models import DoorServiceReport as DoorServiceReportModel
from django.http import JsonResponse
from django.db import transaction
import boto3
from django.conf import settings

class ProjectReport(generics.ListAPIView):
    '''Get all report on a project'''
    serializer_class = ProjectReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = self.kwargs['project']
        return ProjectReportModel.objects.filter(**{"project_id" : project},is_active=True).order_by('-date')

class ProjectReportCreate(generics.ListCreateAPIView):
    serializer_class = ProjectReportCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectReportModel.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class ProjectReportRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectReportCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectReportModel.objects.all()
        
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
            instance: Report instance
        """
        try:
            with transaction.atomic():
                self.destroy_attachments(instance)
                instance.delete()

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'success': 'Report and attachments deleted successfully.'})

class IncidentReport(generics.ListAPIView):
    '''Get all report for a year'''
    serializer_class = IncidentReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # year = self.kwargs['year']
        # return IncidentReportModel.objects.filter(date__year=year).all()
        return IncidentReportModel.objects.order_by('-date')

class IncidentReportCreate(generics.ListCreateAPIView):
    serializer_class = IncidentReportCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncidentReportModel.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class IncidentReportRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncidentReportCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncidentReportModel.objects.all()
        
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
            instance: Report instance
        """
        try:
            with transaction.atomic():
                self.destroy_attachments(instance)
                instance.delete()

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'success': 'Report and attachments deleted successfully.'})

class DoorServiceReport(generics.ListAPIView):
    '''Get all report on a project'''
    serializer_class = DoorServiceReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service = self.kwargs['service']
        return DoorServiceReportModel.objects.filter(**{"service_id" : service},is_active=True).all()

class DoorReportCreate(generics.ListCreateAPIView):
    serializer_class = DoorServiceReportCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorServiceReportModel.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorReportRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorServiceReportCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorServiceReportModel.objects.all()

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
            instance: Report instance
        """
        try:
            with transaction.atomic():
                self.destroy_attachments(instance)
                instance.delete()

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'success': 'Report and attachments deleted successfully.'})