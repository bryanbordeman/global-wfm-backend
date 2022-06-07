from dataclasses import field
from rest_framework import serializers
from task.models import Task
from django.contrib.auth.models import User

class  TaskSerializer(serializers.ModelSerializer):
    '''Announcement serializer'''
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', ]