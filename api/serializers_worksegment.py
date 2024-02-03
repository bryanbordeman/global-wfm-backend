from rest_framework import serializers
from worksegment.models import WorkSegment, WorkType, PTO
from api.serializers_user import MinimalUserSerializer

class  PTOSerializer(serializers.ModelSerializer):
    '''Employee view'''
    class Meta:
        model = PTO
        fields = '__all__'

class PTOApprovedSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    class Meta:
        model = PTO
        fields = ['id']
        read_only_fields = ['PTO_type', 'is_full_day', 'date', 'isoweek', 'duration', 'notes']

class  PTOWeekSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    user=MinimalUserSerializer()
    class Meta:
        model = PTO
        fields = '__all__'
        depth = 2

class  WorkTypeSerializer(serializers.ModelSerializer):
    '''All work types [field, shop, office]'''
    class Meta:
        model = WorkType
        fields = '__all__'

class  WorkSegmentSerializer(serializers.ModelSerializer):
    '''Employee view only'''
    is_approved = serializers.ReadOnlyField()
    class Meta:
        model = WorkSegment
        fields = ['id','user','segment_type', 'project', 'service', 'hse', 'quote','date', 'isoweek', 'is_approved', 'start_time', 'end_time', 'lunch', 'travel_duration', 'duration', 'notes']

class  WorkSegmentDepthSerializer(serializers.ModelSerializer):
    '''Employee view only'''
    is_approved = serializers.ReadOnlyField()
    class Meta:
        model = WorkSegment
        fields = ['id','user','segment_type', 'project', 'service', 'hse', 'quote','date', 'isoweek', 'is_approved', 'start_time', 'end_time', 'lunch', 'travel_duration', 'duration', 'notes']
        depth = 1

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


class  WorkSegmentsProjectInformationSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    user=MinimalUserSerializer()
    class Meta:
        model = WorkSegment
        fields = ['segment_type', 'user','date', 'isoweek', 'start_time', 'end_time', 'lunch', 'travel_duration', 'duration', 'notes']