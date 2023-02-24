from rest_framework import serializers
from announcement.models import Announcement

class  AnnouncementSerializer(serializers.ModelSerializer):
    '''Announcement serializer'''
    class Meta:
        model = Announcement
        fields = ['id','title', 'memo', 'is_active', 'created']