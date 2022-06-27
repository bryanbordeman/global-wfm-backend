from dataclasses import field
from rest_framework import serializers
from task.models import Task
from api.serializers_user import MinimalUserSerializer

class  TaskSerializer(serializers.ModelSerializer):
    '''Task serializer'''
    user = MinimalUserSerializer()
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1