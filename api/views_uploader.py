from rest_framework import generics, permissions
from uploader.models import DropBox
from uploader.models import Drawing
from uploader.models import DrawingType
from .serializers_uploader import DropBoxSerializer
from .serializers_uploader import DrawingSerializer
from .serializers_uploader import DrawingTypeSerializer
import boto3
from django.conf import settings
from django.http import JsonResponse
from django.db import transaction

class DropBoxViewset(generics.ListAPIView):

    serializer_class = DropBoxSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DropBox.objects.all()

class DropBoxCreate(generics.ListCreateAPIView):
    serializer_class = DropBoxSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DropBox.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DropBoxRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DropBoxSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DropBox.objects.all()


class DrawingViewset(generics.ListAPIView):

    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Drawing.objects.all()

class DrawingProject(generics.ListAPIView):

    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Drawing.objects.filter(project_id=project_id, is_active=True).all()

class DrawingService(generics.ListAPIView):

    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return Drawing.objects.filter(service_id=service_id, is_active=True).all()

class DrawingHSE(generics.ListAPIView):

    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hse_id = self.kwargs['hse_id']
        return Drawing.objects.filter(hse_id=hse_id, is_active=True).all()

class DrawingCreate(generics.ListCreateAPIView):
    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Drawing.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DrawingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Drawing.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()
        updated_file = self.request.data.get('document')  # Get the updated file from the request
        print('this is the new file', updated_file)

        # Update other fields if necessary
        instance.rev = serializer.validated_data.get('rev', instance.rev)
        instance.drawing_type = serializer.validated_data.get('drawing_type', instance.drawing_type)
        instance.title_suffix = serializer.validated_data.get('title_suffix', instance.title_suffix)

        if updated_file:
            # Save the updated file
            instance.document.content_type = 'application/pdf'
            instance.document.save(updated_file.name, updated_file)
        else:
            print('inside else statment')
            # Keep the original file by setting document field to its existing value
            serializer.validated_data['document'] = instance.document

        print('before save')
        instance.save()


    def perform_destroy(self, instance):

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        file_field = instance.document  # Retrieve the FieldFile object
        file_path = str(file_field)  # Convert the FieldFile object to a string (file path)

        try:
            s3.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_path
            )
            with transaction.atomic():
                instance.delete()  # Delete the database instance

        except Exception as e:
            print("Exception:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

class DrawingTypeView(generics.ListAPIView):

    serializer_class = DrawingTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DrawingType.objects.all()

class DrawingTypeCreate(generics.ListCreateAPIView):
    serializer_class = DrawingTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DrawingType.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DrawingTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrawingTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DrawingType.objects.all()