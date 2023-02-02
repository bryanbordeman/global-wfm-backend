from rest_framework import generics, permissions
from .serializers_vehicle import VehicleSerializer
from schedule.models import Vehicle as VehicleModel

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

