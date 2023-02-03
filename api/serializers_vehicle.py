from rest_framework import serializers
from schedule.models import Vehicle, VehicleIssue, VehicleService, VehicleInspection, VehicleCleaning
from api.serializers_user import UserSerializer

class  VehicleSerializer(serializers.ModelSerializer):
    '''Vehicle serializer'''
    assignment = UserSerializer()
    class Meta:
        model = Vehicle
        fields = '__all__'
        depth = 1

class  VehicleIssueSerializer(serializers.ModelSerializer):
    '''Vehicle Issue serializer'''
    created_by = UserSerializer()
    class Meta:
        model = VehicleIssue
        fields = '__all__'
        depth = 1

class  CreateVehicleIssueSerializer(serializers.ModelSerializer):
    '''Create Vehicle Issue serializer'''
    class Meta:
        model = VehicleIssue
        fields = '__all__'

class  VehicleServiceSerializer(serializers.ModelSerializer):
    '''Vehicle Service serializer'''
    created_by = UserSerializer()
    class Meta:
        model = VehicleService
        fields = '__all__'
        depth = 1

class  CreateVehicleServiceSerializer(serializers.ModelSerializer):
    '''Create Vehicle Service serializer'''
    class Meta:
        model = VehicleService
        fields = '__all__'

class  VehicleInspectionSerializer(serializers.ModelSerializer):
    '''Vehicle Inspection serializer'''
    created_by = UserSerializer()
    class Meta:
        model = VehicleInspection
        fields = '__all__'
        depth = 1

class  CreateVehicleInspectionSerializer(serializers.ModelSerializer):
    '''Create Vehicle Inspection serializer'''
    class Meta:
        model = VehicleInspection
        fields = '__all__'

class  VehicleCleaningSerializer(serializers.ModelSerializer):
    '''Vehicle Inspection serializer'''
    created_by = UserSerializer()
    class Meta:
        model = VehicleCleaning
        fields = '__all__'
        depth = 1

class  CreateVehicleCleaningSerializer(serializers.ModelSerializer):
    '''Create Vehicle Inspection serializer'''
    class Meta:
        model = VehicleCleaning
        fields = '__all__'