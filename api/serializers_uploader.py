from rest_framework import serializers
from uploader.models import DropBox
from uploader.models import Drawing
from uploader.models import DrawingType

class DropBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = DropBox
        fields = '__all__'

class DrawingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drawing
        fields = '__all__'

        def get_document(self, obj):
            return str(obj.document)

class DrawingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DrawingType
        fields = '__all__'