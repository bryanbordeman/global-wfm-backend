from rest_framework import generics, permissions
from .serializers_project import ProjectSerializer, ProjectCreateSerializer
from .serializers_project import ProjectCategorySerializer, ProjectTypeSerializer
from .serializers_project import BillingTypeSerializer, OrderTypeSerializer
from project.models import Project as ProjectModel
from project.models import ProjectCategory as ProjectCategoryModel
from project.models import ProjectType as ProjectTypeModel
from project.models import BillingType as BillingTypeModel
from project.models import OrderType as OrderTypeModel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import time


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


@csrf_exempt
def NextProjectNumber(request):
    '''Get the Next Project Number'''
    year = time.strftime("%Y")[2:]
    if request.method == 'GET':
        #! what if its not sequential and we manually enter old quote or database is empty?? 
        last_project = model_to_dict(ProjectModel.objects.filter(is_active=True).order_by('-number').first())
        
        last_project_number = (last_project['number'])
        current_project_year = last_project_number[-2:]

        if current_project_year == year:
            next_number = int(last_project_number[:3])+1
            next_number_str = f'{next_number}{current_project_year}'
        else:
            next_number = '100'
            next_number_str = f'{next_number}{year}'

        return JsonResponse({'next_project_number': str(next_number_str)}, status=201)

@csrf_exempt
def LastProject(request):
    '''Get the Last Quote Number'''
    if request.method == 'GET':
        last_project = model_to_dict(ProjectModel.objects.filter(is_active=True).order_by('-number').first())
        
        last_project_id = (last_project['id'])

        return JsonResponse({'last_project_id': str(last_project_id)}, status=201)