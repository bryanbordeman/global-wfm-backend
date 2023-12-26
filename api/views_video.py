from rest_framework import generics, permissions
from uploader.models import Video
from uploader.models import VideoCategory
from uploader.models import VideoThumbnail
from .serializers_video import VideoSerializer
from .serializers_video import VideoCategorySerializer
from .serializers_video import VideoThumbnailSerializer

import boto3
from django.conf import settings
from django.http import JsonResponse
from django.db import transaction

class VideoViewset(generics.ListAPIView):

    serializer_class = VideoSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Video.objects.all()

class VideoCreate(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Video.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class VideoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VideoSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Video.objects.all()
    
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


class VideoThumbnailViewset(generics.ListAPIView):

    serializer_class = VideoThumbnailSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VideoThumbnail.objects.all()

class VideoThumbnailCreate(generics.ListCreateAPIView):
    serializer_class = VideoThumbnail
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VideoThumbnail.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class VideoThumbnailRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VideoThumbnail
    permissions_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return VideoThumbnail.objects.all()

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

class VideoCategoryViewset(generics.ListAPIView):

    serializer_class = VideoCategorySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VideoCategory.objects.all()

class VideoCategoryCreate(generics.ListCreateAPIView):
    serializer_class = VideoCategorySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VideoCategory.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class VideoCategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VideoCategorySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VideoCategory.objects.all()