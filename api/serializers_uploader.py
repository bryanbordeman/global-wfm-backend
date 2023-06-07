from rest_framework import serializers
from uploader.models import DropBox
from uploader.models import Drawing
from uploader.models import DrawingType
from drf_extra_fields.fields import Base64FileField
import PyPDF2
import io

class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
        except PyPDF2.utils.PdfReadError as e:
            print(e)
        else:
            return 'pdf'

class DropBoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = DropBox
        fields = '__all__'

class DrawingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Drawing
        fields = '__all__'

class DrawingTypeSerializer(serializers.ModelSerializer):
    document = Base64FileField(max_length=None, use_url=True)
    class Meta:
        model = DrawingType
        fields = '__all__'