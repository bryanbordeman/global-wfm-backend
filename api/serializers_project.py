from rest_framework import serializers
from project.models import Project

class  ProjectSerializer(serializers.ModelSerializer):
    '''Project serializer'''
    class Meta:
        model = Project
        fields = '__all__'
        depth = 3

class MinimalProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'number', 'name', 'is_active' ]

class  ProjectCreateSerializer(serializers.ModelSerializer):
    ''' Create Project serializer'''
    is_active = serializers.BooleanField(initial=True)
    class Meta:
        model = Project
        fields = '__all__'