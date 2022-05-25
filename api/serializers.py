from rest_framework import serializers
from worksegment.models import WorkSegment
from announcement.models import Announcement

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

class  AnnouncementSerializer(serializers.ModelSerializer):
    '''Announcement serializer'''
    class Meta:
        model = Announcement
        fields = '__all__'