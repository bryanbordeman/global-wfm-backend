from rest_framework import generics, permissions
from .serializers_employee import EmployeeSerializer, EmployeeUpdateSerializer
from .serializers_employee import EmployeeRateSerializer, EmployeeRateUpdateSerializer
from employee.models import Employee as EmployeeModel
from employee.models import EmployeeRate as EmployeeRateModel
from collections import defaultdict
from rest_framework.response import Response

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

class EmployeeRate(generics.ListAPIView):
    '''Contact view'''
    serializer_class = EmployeeRateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeRateModel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = defaultdict(list)
        for rate in queryset:
            key = (rate.employee.id)  # employee ID is the key
            data[key].append(self.get_serializer(rate).data)
        return Response(data)
    
class EmployeeRateCreate(generics.ListCreateAPIView):
    serializer_class = EmployeeRateUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeRateModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class EmployeeRateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeRateUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeRateModel.objects.all()  
