from rest_framework import serializers
from worksegment.models import WorkSegment

class  WorkSegmentSerializer(serializers.ModelSerializer):
    '''Employee view only'''
    is_approved = serializers.ReadOnlyField()
    class Meta:
        model = WorkSegment
        fields = ['project', 'date', 'isoweek', 'is_approved', 'start_time', 'end_time', 'lunch', 'travel_duration', 'duration', 'notes']

class WorkSegmentApprovedSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    class Meta:
        model = WorkSegment
        fields = ['id']
        read_only_fields = ['project', 'date', 'isoweek', 'start_time', 'end_time', 'lunch', 'travel_duration', 'duration', 'notes']

class  WorkSegmentsWeekSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    class Meta:
        model = WorkSegment
        fields = '__all__'