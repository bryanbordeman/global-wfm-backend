from rest_framework import generics, permissions
from .serializers_employee import EmployeeSerializer, EmployeeUpdateSerializer
from employee.models import Employee as EmployeeModel

class Employee(generics.ListAPIView):
    '''Contact view'''
    serializer_class = EmployeeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeModel.objects.filter(user__is_active=True).order_by('user__last_name')

class EmployeeCreate(generics.ListCreateAPIView):
    serializer_class = EmployeeUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeModel.objects.all()