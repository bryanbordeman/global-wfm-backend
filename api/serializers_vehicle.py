from rest_framework import serializers
from schedule.models import Vehicle
from api.serializers_user import UserSerializer

class  VehicleSerializer(serializers.ModelSerializer):
    '''Vehicle serializer'''
    assignment = UserSerializer()
    class Meta:
        model = Vehicle
        fields = '__all__'
        depth = 1