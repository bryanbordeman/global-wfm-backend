from rest_framework import generics, permissions
from .serializers_project import ProjectSerializer
from project.models import Project as ProjectModel

class Project(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ProjectSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectModel.objects.filter(is_active=True).order_by('-number')

# class AnnouncementCreate(generics.ListCreateAPIView):
#     serializer_class = AnnouncementSerializer
#     permissions_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return AnnouncementModel.objects.all()
    
#     def perform_create(self, serializer):
#         serializer.save()

# class AnnouncementRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = AnnouncementSerializer
#     permissions_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return AnnouncementModel.objects.all()
