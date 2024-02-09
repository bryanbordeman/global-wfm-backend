from rest_framework import serializers
from employee.models import Employee
from employee.models import EmployeeBenefit
from employee.models import Benefit
from employee.models import EmployeeRate
from employee.models import PrevailingRate
from api.serializers_user import MinimalUserSerializer
from api.serializers_project import MinimalProjectSerializer


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

        def get_employee(self, obj):
            return str(obj.employee)

class EmployeeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRate
        fields = '__all__'
        depth = 1

class EmployeeSerializer(serializers.ModelSerializer):
    user=MinimalUserSerializer()
    employeebenefit_set = EmployeeBenefitSerializer(many=True, read_only=True)
    employeerate_set = EmployeeRateSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'user', 'start_date', 'is_salary', 'notes', 'documents', 'vacation_hours', 'holiday_hours', 'sick_hours', 'employeebenefit_set', 'employeerate_set']
        depth = 1
        
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