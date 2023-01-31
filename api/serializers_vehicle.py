from rest_framework import serializers
from schedule.models import Vehicle

class  VehicleSerializer(serializers.ModelSerializer):
    '''Vehicle serializer'''
    class Meta:
        model = Vehicle
        fields = '__all__'