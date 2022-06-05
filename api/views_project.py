from rest_framework import generics, permissions
from .serializers_project import ProjectSerializer, ProjectCreateSerializer
from project.models import Project as ProjectModel

class Project(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ProjectSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectModel.objects.filter(is_active=True).order_by('-number')

class ProjectCreate(generics.ListCreateAPIView):
    serializer_class = ProjectCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectModel.objects.all()
    
    def perform_create(self, serializer):
        number = self.request.POST['number']
        if ProjectModel.objects.filter(number=number).exists():
            return print('Project number already exist')
        else:
            serializer.save()

        

class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectModel.objects.all()
