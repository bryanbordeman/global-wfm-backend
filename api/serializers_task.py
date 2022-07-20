from dataclasses import field
from rest_framework import serializers
from task.models import Task, TaskList, SubTask
from api.serializers_user import MinimalUserSerializer
from api.serializers_project import MinimalProjectSerializer

class  TaskSerializer(serializers.ModelSerializer):
    '''Task serializer'''
    created_by = MinimalUserSerializer()
    assignee = MinimalUserSerializer()
    project = MinimalProjectSerializer()
    
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1

class  TaskCreateSerializer(serializers.ModelSerializer):
    '''Create Task serializer'''
    class Meta:
        model = Task
        fields = '__all__'


class  TaskListSerializer(serializers.ModelSerializer):
    '''Task List serializer'''

    class Meta:
        model = TaskList
        fields = '__all__'

class  SubTaskSerializer(serializers.ModelSerializer):
    '''SubTask serializer'''

    class Meta:
        model = SubTask
        fields = '__all__'

class SubTaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id']
        read_only_fields = ['title', 'notes', 'is_complete', 'completed', 'updated']