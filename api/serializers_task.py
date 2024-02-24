from rest_framework import serializers
from task.models import Task, TaskList, SubTask
from api.serializers_user import MinimalUserSerializer
from api.serializers_project import MinimalProjectSerializer
from api.serializers_uploader import DropBoxSerializer

class  TaskSerializer(serializers.ModelSerializer):
    '''Task serializer'''
    created_by = MinimalUserSerializer()
    assignee = MinimalUserSerializer()
    project = MinimalProjectSerializer()
    
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1

class TaskCreateSerializer(serializers.ModelSerializer):
    '''Create Task serializer'''

    attachments = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['attachments'] = DropBoxSerializer(instance.attachments.all(), many=True).data
        return representation

class  TaskListSerializer(serializers.ModelSerializer):
    '''Task List serializer'''

    class Meta:
        model = TaskList
        fields = '__all__'

class TaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = ['id']
        read_only_fields = ['title', 'notes', 'is_complete', 'is_read', 'is_public','completed', 'updated']

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