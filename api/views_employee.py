from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers_employee import EmployeeSerializer, EmployeeUpdateSerializer
from .serializers_employee import EmployeeRateSerializer, EmployeeRateUpdateSerializer
from .serializers_employee import PrevailingRateSerializer, PrevailingRateUpdateSerializer
from .serializers_employee import BenefitSerializer, EmployeeBenefitSerializer, EmployeeBenefitUpdateSerializer
from .serializers_employee import SickAccrualOverrideSerializer
from employee.models import SickAccrualOverride as SickAccrualOverrideModel
from employee.models import Employee as EmployeeModel
from employee.models import EmployeeRate as EmployeeRateModel
from employee.models import Benefit as BenefitModel
from employee.models import EmployeeBenefit as EmployeeBenefitModel
from employee.models import PrevailingRate as PrevailingRateModel

from collections import defaultdict
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from employee.models import EmployeeHoursSettings
from .serializers_employee import EmployeeHoursSettingsSerializer 

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

class EmployeeDetailView(generics.RetrieveAPIView):
    serializer_class = EmployeeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user__id=self.kwargs["pk"])
        return obj

    def get_queryset(self):
        return EmployeeModel.objects.all()

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

class EmployeeHoursSettingsView(generics.RetrieveUpdateAPIView):
    queryset = EmployeeHoursSettings.objects.all()
    serializer_class = EmployeeHoursSettingsSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        EmployeeModel.objects.update(sick_hours=instance.sick_hours, holiday_hours=instance.holiday_hours)

    def get_object(self):
        return EmployeeHoursSettings.load()
    
class SickAccrualOverrideList(generics.ListAPIView):
    serializer_class = SickAccrualOverrideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        employee_id = int(self.kwargs['employee'])
        return SickAccrualOverrideModel.objects.filter(employee__user__is_active=True, employee__id=employee_id).all()
        
class SickAccrualOverrideCreate(generics.ListCreateAPIView):
    serializer_class = SickAccrualOverrideSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SickAccrualOverrideModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class SickAccrualOverrideRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SickAccrualOverrideSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SickAccrualOverrideModel.objects.all()