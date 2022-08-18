from rest_framework import serializers
from project.models import Project, ProjectCategory, ProjectType

class  ProjectCategorySerializer(serializers.ModelSerializer):
    '''Project Category serializer'''
    class Meta:
        model = ProjectCategory
        fields = '__all__'

class  ProjectTypeSerializer(serializers.ModelSerializer):
    '''Project Type serializer'''
    class Meta:
        model = ProjectType
        fields = '__all__'

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