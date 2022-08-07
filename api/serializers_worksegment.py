from rest_framework import serializers
from worksegment.models import WorkSegment
from api.serializers_user import MinimalUserSerializer

class  WorkSegmentSerializer(serializers.ModelSerializer):
    '''Employee view only'''
    is_approved = serializers.ReadOnlyField()
    class Meta:
        model = WorkSegment
        fields = ['user','segment_type', 'project', 'date', 'isoweek', 'is_approved', 'start_time', 'end_time', 'lunch', 'travel_duration', 'duration', 'notes']

class WorkSegmentApprovedSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    class Meta:
        model = WorkSegment
        fields = ['id']
        read_only_fields = ['segment_type', 'project', 'date', 'isoweek', 'start_time', 'end_time', 'lunch', 'travel_duration', 'duration', 'notes']

class  WorkSegmentsWeekSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    user=MinimalUserSerializer()
    class Meta:
        model = WorkSegment
        fields = '__all__'
        depth = 2