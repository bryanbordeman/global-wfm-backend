from rest_framework import generics, permissions
from .serializers_vehicle import VehicleSerializer 
from .serializers_vehicle import VehicleIssueSerializer
from .serializers_vehicle import VehicleInspectionSerializer
from .serializers_vehicle import VehicleServiceSerializer
from .serializers_vehicle import VehicleCleaningSerializer

from .serializers_vehicle import CreateVehicleIssueSerializer
from .serializers_vehicle import CreateVehicleInspectionSerializer
from .serializers_vehicle import CreateVehicleServiceSerializer
from .serializers_vehicle import CreateVehicleCleaningSerializer

from schedule.models import Vehicle as VehicleModel
from schedule.models import VehicleIssue as VehicleIssueModel
from schedule.models import VehicleInspection as VehicleInspectionModel
from schedule.models import VehicleService as VehicleServiceModel
from schedule.models import VehicleCleaning as VehicleCleaningModel

import datetime 

today = datetime.datetime.now() 
last_year = datetime.datetime.now() - datetime.timedelta(days=1*365)

class Vehicle(generics.ListAPIView):
    '''Employee view'''
    serializer_class = VehicleSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleModel.objects.all().order_by('-id')

class VehicleCreate(generics.ListCreateAPIView):
    serializer_class = VehicleSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class VehicleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleModel.objects.all()

#!------------------------------------------------------------------

class VehicleIssue(generics.ListAPIView):
    '''Employee view'''
    serializer_class = VehicleIssueSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleIssueModel.objects.filter(is_resolved=False).order_by('-date')

class VehicleIssueCreate(generics.ListCreateAPIView):
    serializer_class = CreateVehicleIssueSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleIssueModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class VehicleIssueRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateVehicleIssueSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleIssueModel.objects.all()

#!------------------------------------------------------------------

class VehicleInspection(generics.ListAPIView):
    '''Employee view'''
    serializer_class = VehicleInspectionSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return VehicleInspectionModel.objects.filter(date__gte=last_year).filter(date__lte=today).order_by('-date')
        return VehicleInspectionModel.objects.order_by('expiration_date')

class VehicleInspectionCreate(generics.ListCreateAPIView):
    serializer_class = CreateVehicleInspectionSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleInspectionModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class VehicleInspectionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateVehicleInspectionSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleInspectionModel.objects.all()

#!------------------------------------------------------------------

class VehicleService(generics.ListAPIView):
    '''Employee view'''
    serializer_class = VehicleServiceSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return VehicleServiceModel.objects.filter(date__year=year).order_by('-vehicle')

class VehicleServiceCreate(generics.ListCreateAPIView):
    serializer_class = CreateVehicleServiceSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleServiceModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class VehicleServiceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateVehicleServiceSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleServiceModel.objects.all()

#!------------------------------------------------------------------

class VehicleCleaning(generics.ListAPIView):
    '''Employee view'''
    serializer_class = VehicleCleaningSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return VehicleCleaningModel.objects.filter(date__year=year).order_by('-date')

class VehicleCleaningCreate(generics.ListCreateAPIView):
    serializer_class = CreateVehicleCleaningSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleCleaningModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class VehicleCleaningRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateVehicleCleaningSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleCleaningModel.objects.all()

