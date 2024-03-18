from rest_framework import serializers
from employee.models import Employee
from employee.models import EmployeeBenefit
from employee.models import Benefit
from employee.models import EmployeeRate
from employee.models import PrevailingRate
from employee.models import EmployeeHoursSettings
from employee.models import SickAccrualOverride
from api.serializers_user import MinimalUserSerializer
from api.serializers_project import MinimalProjectSerializer

from rest_framework.fields import SerializerMethodField
from django.utils import timezone
from worksegment.models import PTO as PTOModel
from worksegment.models import WorkSegment
from django.db.models import Sum
from datetime import date
import math
from decimal import Decimal

class SickAccrualOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = SickAccrualOverride
        fields = '__all__'

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

    sick_accrualed_list = SerializerMethodField()
    sick_accrualed = SerializerMethodField()
    sick_hours_year = SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'start_date', 'is_salary', 'is_full_time', 'notes', 'documents', 'vacation_hours', 'holiday_hours', 'sick_hours', 'years_worked', 'eligible_vacation_hours', 'vacation_accrual_multiplier','vacation_accrualed', 'employeebenefit_set', 'employeerate_set', 'vacation_hours_year', 'sick_accrualed_list', 'sick_accrualed', 'sick_hours_year']
        depth = 1
    
    def get_sick_accrualed_list(self, obj):
        # Check if the employee has a SickAccrualOverride
        sick_accrual_override = SickAccrualOverride.objects.filter(employee=obj).first()

        start_date = sick_accrual_override.start_date if sick_accrual_override else obj.start_date
        start_year = start_date.year
        current_year = date.today().year

        carry_over = 0
        sick_accrualed_per_year = []

        # Loop over each year from the start year to the current year
        for year in range(start_year, current_year + 1):
            if year == start_year:
                start_date_year = start_date
                sick_accrualed_year = sick_accrual_override.sick_accrualed if sick_accrual_override else 0
            else:
                start_date_year = date(year, 1, 1)
                sick_accrualed_year = 0

            if year == current_year:
                end_date_year = date.today()
            else:
                end_date_year = date(year, 12, 31)

            # Calculate total hours worked in the year
            work_segments = WorkSegment.objects.filter(user=obj.user, is_approved=True, date__gte=start_date_year, date__lte=end_date_year)
            total_duration_worked_year = sum(segment.duration for segment in work_segments)

            # Calculate sick hours used in the year
            PTO = PTOModel.objects.filter(user=obj.user, date__gte=start_date_year, date__lte=end_date_year, PTO_type='Sick')
            sick_hours_used = PTO.aggregate(Sum('duration'))['duration__sum'] or 0

            # Add the carry over from the previous year to the current year's accrued sick time
            sick_accrualed_year += carry_over

            # Calculate the sick hours accrued
            sick_accrualed_year += Decimal(total_duration_worked_year / 30)

            # Subtract the sick hours used from the sick hours accrued
            sick_accrualed_year -= Decimal(sick_hours_used)

            # At the end of the year, carry over up to 40 sick hours accrued to the next year. Also, if hours are negative this will carry over.
            if sick_accrualed_year > 40:
                carry_over = sick_accrualed_year - 40
                sick_accrualed_year = 40
            else:
                carry_over = sick_accrualed_year

            # Add the year's data to the list
            sick_accrualed_per_year.append({
                'year': year,
                'total_duration_worked_year': total_duration_worked_year,
                'sick_hours_used': sick_hours_used,
                'sick_accrualed_year': sick_accrualed_year,
                'carry_over': carry_over
            })

        return sick_accrualed_per_year

    def get_sick_accrualed(self, obj):
        # Check if the difference between start_date and the current date is less than 120 days
        if (date.today() - obj.start_date).days < 120:
            return 0

        sick_accrualed_list = self.get_sick_accrualed_list(obj)
        if sick_accrualed_list:
            return math.ceil(sick_accrualed_list[-1]['sick_accrualed_year'])
        else:
            return 0
        
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