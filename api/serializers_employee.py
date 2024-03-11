from rest_framework import serializers
from employee.models import Employee
from employee.models import EmployeeBenefit
from employee.models import Benefit
from employee.models import EmployeeRate
from employee.models import PrevailingRate
from employee.models import EmployeeHoursSettings
from api.serializers_user import MinimalUserSerializer
from api.serializers_project import MinimalProjectSerializer

from rest_framework.fields import SerializerMethodField
from django.utils import timezone
from worksegment.models import PTO as PTOModel
from worksegment.models import WorkSegment
from django.db.models import Sum
from datetime import date
import math

from django.db.models.functions import ExtractWeek

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'

class EmployeeBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBenefit
        fields = '__all__'
        depth = 1

class EmployeeBenefitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBenefit
        fields = '__all__'

class EmployeeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRate
        fields = '__all__'
        depth = 1

class EmployeeSerializer(serializers.ModelSerializer):
    years_worked = serializers.IntegerField(read_only=True)
    eligible_vacation_hours = serializers.IntegerField(read_only=True)
    vacation_accrual_multiplier = serializers.DecimalField(max_digits=7, decimal_places=4, read_only=True)
    vacation_accrualed = serializers.IntegerField(read_only=True)

    user=MinimalUserSerializer()
    employeebenefit_set = EmployeeBenefitSerializer(many=True, read_only=True)
    employeerate_set = EmployeeRateSerializer(many=True, read_only=True)

    vacation_hours_year = SerializerMethodField()
    sick_hours_year = SerializerMethodField()

    sick_accrualed = SerializerMethodField()
    total_hours = SerializerMethodField()
    sick_previous_year = SerializerMethodField()


    class Meta:
        model = Employee
        fields = ['id', 'user', 'start_date', 'is_salary', 'is_full_time', 'notes', 'documents', 'vacation_hours', 'holiday_hours', 'sick_hours', 'years_worked', 'eligible_vacation_hours', 'vacation_accrual_multiplier','vacation_accrualed', 'employeebenefit_set', 'employeerate_set', 'vacation_hours_year', 'sick_hours_year', 'sick_accrualed', 'sick_previous_year', 'total_hours']
        depth = 1

    def get_total_hours(self, obj):
        current_year = timezone.now().year
        work_segments = WorkSegment.objects.filter(user=obj.user, is_approved=True, date__year=current_year)
        work_segments = work_segments.annotate(week=ExtractWeek('date')).values('week').annotate(total_duration=Sum('duration')).order_by('week')
        total_duration = sum(segment['total_duration'] for segment in work_segments)
        return total_duration

    def get_sick_previous_year(self, obj):
        previous_year = timezone.now().year - 1
        PTO = PTOModel.objects.filter(user=obj.user, date__year=previous_year, PTO_type='Sick')
        sick_hours = PTO.aggregate(Sum('duration'))['duration__sum'] or 0

        # Calculate remaining sick hours from the previous year
        remaining_from_previous_year = max(40 - sick_hours, 0)
        return remaining_from_previous_year

    def get_sick_accrualed(self, obj):
        days_since_start = (date.today() - obj.start_date).days

        if days_since_start < 120:
            return 0

        previous_year = self.get_sick_previous_year(obj)
        total_duration = self.get_total_hours(obj)
        sick_accrualed = min(math.ceil(total_duration / 30), 40)
        
        # Add remaining sick hours from the previous year to sick_accrualed
        sick_accrualed += min(previous_year, 40 - sick_accrualed)

        # Ensure sick_accrualed does not exceed 40
        sick_accrualed = min(sick_accrualed, 40)

        return sick_accrualed

    def get_vacation_hours_year(self, obj):
        current_year = timezone.now().year
        PTO = PTOModel.objects.filter(user=obj.user, date__year=current_year, PTO_type='Vacation')
        vacation_hours = PTO.aggregate(Sum('duration'))['duration__sum'] or 0
        return vacation_hours

    def get_sick_hours_year(self, obj):
        current_year = timezone.now().year
        PTO = PTOModel.objects.filter(user=obj.user, date__year=current_year, PTO_type='Sick')
        sick_hours = PTO.aggregate(Sum('duration'))['duration__sum'] or 0
        return sick_hours

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeRateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRate
        fields = '__all__'

class PrevailingRateSerializer(serializers.ModelSerializer):
    project = MinimalProjectSerializer()

    class Meta:
        model = PrevailingRate
        fields = '__all__'
        depth = 2

class PrevailingRateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrevailingRate
        fields = '__all__'

class EmployeeHoursSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeHoursSettings
        fields = ['sick_hours', 'holiday_hours']