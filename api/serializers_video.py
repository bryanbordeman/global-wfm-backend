from rest_framework import serializers
from uploader.models import Video, VideoCategory, VideoThumbnail
from api.serializers_expense import Base64ImageField


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = '__all__'

class VideoThumbnailSerializer(serializers.ModelSerializer):
    document = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = VideoThumbnail
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'
        depth = 1

    def get_document(self, obj):
            return str(obj.document)