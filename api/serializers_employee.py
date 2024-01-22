from rest_framework import serializers
from employee.models import Employee
from api.serializers_user import MinimalUserSerializer

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