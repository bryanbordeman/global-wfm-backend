from rest_framework import generics, permissions
from .serializers_announcement import AnnouncementSerializer
from announcement.models import Announcement as AnnouncementModel

class Announcement(generics.ListAPIView):
    '''Employee view'''
    serializer_class = AnnouncementSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnnouncementModel.objects.filter(is_active=True).order_by('-created')

class AnnouncementCreate(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnnouncementModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class AnnouncementRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnouncementSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnnouncementModel.objects.all()
