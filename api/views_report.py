from rest_framework import generics, permissions
from .serializers_report import ProjectReportSerializer, IncidentReportSerializer, DoorServiceReportSerializer
from report.models import ProjectReport as ProjectReportModel
from report.models import IncidentReport as IncidentReportModel
from report.models import DoorServiceReport as DoorServiceReportModel

class ProjectReport(generics.ListAPIView):
    '''Get all report on a project'''
    serializer_class = ProjectReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = self.kwargs['project']
        return ProjectReportModel.objects.filter(**{"project_id" : project},is_active=True).all()

class ProjectReportCreate(generics.ListCreateAPIView):
    serializer_class = ProjectReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectReportModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class ProjectReportRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectReportModel.objects.all()
    
class IncidentReport(generics.ListAPIView):
    '''Get all report for a year'''
    serializer_class = IncidentReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncidentReportModel.objects.all()

class IncidentReportCreate(generics.ListCreateAPIView):
    serializer_class = IncidentReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncidentReportModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class IncidentReportRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncidentReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncidentReportModel.objects.all()
    
class DoorServiceReport(generics.ListAPIView):
    '''Get all report on a project'''
    serializer_class = DoorServiceReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service = self.kwargs['service']
        return DoorServiceReportModel.objects.filter(**{"service_id" : service},is_active=True).all()

class DoorReportCreate(generics.ListCreateAPIView):
    serializer_class = DoorServiceReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorServiceReportModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class DoorReportRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorServiceReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorServiceReportModel.objects.all()