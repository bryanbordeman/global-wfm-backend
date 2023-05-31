from rest_framework import serializers
from uploader.models import DropBox
from uploader.models import Drawing


class DropBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = DropBox
        fields = '__all__'

class DrawingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drawing
        fields = '__all__'