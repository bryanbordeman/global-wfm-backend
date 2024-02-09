from rest_framework import generics, permissions
from .serializers_employee import EmployeeSerializer, EmployeeUpdateSerializer
from .serializers_employee import EmployeeRateSerializer, EmployeeRateUpdateSerializer
from .serializers_employee import PrevailingRateSerializer, PrevailingRateUpdateSerializer
from .serializers_employee import BenefitSerializer, EmployeeBenefitSerializer, EmployeeBenefitUpdateSerializer
from employee.models import Employee as EmployeeModel
from employee.models import EmployeeRate as EmployeeRateModel
from employee.models import Benefit as BenefitModel
from employee.models import EmployeeBenefit as EmployeeBenefitModel
from employee.models import PrevailingRate as PrevailingRateModel
from collections import defaultdict
from rest_framework.response import Response

class Benefit(generics.ListAPIView):
    serializer_class = BenefitSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BenefitModel.objects.all()

class EmployeeBenefit(generics.ListAPIView):
    serializer_class = EmployeeBenefitSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeBenefitModel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = defaultdict(list)
        for benefit in queryset:
            key = (benefit.employee.id)  # employee ID is the key
            data[key].append(self.get_serializer(benefit).data)
        return Response(data)
    
class EmployeeBenefitCreate(generics.ListCreateAPIView):
    serializer_class = EmployeeBenefitUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeBenefitModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class EmployeeBenefitRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeBenefitUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EmployeeBenefitModel.objects.all()
    
class Employee(generics.ListAPIView):
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
    

class PrevailingRate(generics.ListAPIView):
    serializer_class = PrevailingRateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = self.kwargs['project']
        return PrevailingRateModel.objects.filter(**{"project_id" : project}).order_by('effective_date')

class PrevailingRateCreate(generics.ListCreateAPIView):
    serializer_class = PrevailingRateUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrevailingRateModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class PrevailingRateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrevailingRateUpdateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrevailingRateModel.objects.all()  



