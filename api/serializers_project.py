from rest_framework import serializers
from project.models import Project

class  ProjectSerializer(serializers.ModelSerializer):
    '''Project serializer'''
    class Meta:
        model = Project
        fields = '__all__'
        depth = 3
