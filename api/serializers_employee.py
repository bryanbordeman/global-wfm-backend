from rest_framework import serializers
from employee.models import Employee, EmployeeRate, PrevailingRate
from api.serializers_user import MinimalUserSerializer
from api.serializers_project import MinimalProjectSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    user=MinimalUserSerializer()
    class Meta:
        model = Employee
        fields = '__all__'
        depth = 1

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRate
        fields = '__all__'
        depth = 1

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