from rest_framework import generics, permissions
from .serializers_vehicle import VehicleSerializer 
from .serializers_vehicle import VehicleIssueSerializer
from .serializers_vehicle import VehicleInspectionSerializer
from .serializers_vehicle import VehicleServiceSerializer
from .serializers_vehicle import VehicleCleaning

from .serializers_vehicle import CreateVehicleIssueSerializer
from .serializers_vehicle import CreateVehicleInspectionSerializer
from .serializers_vehicle import CreateVehicleServiceSerializer
from .serializers_vehicle import CreateVehicleCleaningSerializer

from schedule.models import Vehicle as VehicleModel
from schedule.models import VehicleIssue as VehicleIssueModel
from schedule.models import VehicleInspection as VehicleInspectionModel
from schedule.models import VehicleService as VehicleServiceModel
from schedule.models import VehicleCleaning as VehicleCleaningModel

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

#------------------------------------------------------------------

class VehicleIssue(generics.ListAPIView):
    '''Employee view'''
    serializer_class = VehicleIssueSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleIssueModel.objects.all().order_by('-date')

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
