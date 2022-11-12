from rest_framework import generics, permissions
from .serializers_project import ProjectSerializer, ProjectCreateSerializer
from .serializers_project import ProjectCategorySerializer, ProjectTypeSerializer
from .serializers_project import BillingTypeSerializer, OrderTypeSerializer
from project.models import Project as ProjectModel
from project.models import ProjectCategory as ProjectCategoryModel
from project.models import ProjectType as ProjectTypeModel
from project.models import BillingType as BillingTypeModel
from project.models import OrderType as OrderTypeModel


class ProjectCategory(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ProjectCategorySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectCategoryModel.objects.all()

class ProjectType(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ProjectTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectTypeModel.objects.all()

class ProjectCategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectCategorySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectCategoryModel.objects.all()

class ProjectTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectTypeModel.objects.all()

class BillingType(generics.ListAPIView):
    '''Employee view'''
    serializer_class = BillingTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BillingTypeModel.objects.all()

class OrderType(generics.ListAPIView):
    '''Employee view'''
    serializer_class = OrderTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderTypeModel.objects.all()



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
