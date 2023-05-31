from rest_framework import generics, permissions
from .serializers_project import ProjectSerializer, ProjectCreateSerializer
from .serializers_project import ServiceSerializer, ServiceCreateSerializer
from .serializers_project import HSESerializer, HSECreateSerializer
from .serializers_project import ProjectCategorySerializer, ProjectTypeSerializer
from .serializers_project import ProjectToggleSerializer
from .serializers_project import ServiceToggleSerializer
from .serializers_project import HSEToggleSerializer
from .serializers_project import BillingTypeSerializer, OrderTypeSerializer
from .serializers_project import MinimalProjectSerializer
from project.models import Project as ProjectModel
from project.models import Service as ServiceModel
from project.models import HSE as HSEModel
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
        return ProjectModel.objects.filter(is_active=True).order_by('-id')
    
class MinimalProject(generics.ListAPIView):
    '''Customer view'''
    serializer_class = MinimalProjectSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return ProjectModel.objects.filter(is_active=True).order_by('-id')

class ProjectYear(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ProjectSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return ProjectModel.objects.filter(is_active=True, created__year=year).order_by('-number')

class ProjectArchive(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ProjectSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return ProjectModel.objects.filter(is_active=False, created__year=year).order_by('-number')

class ProjectToggleArchive(generics.UpdateAPIView):
    '''Toggle Archive'''
    serializer_class = ProjectToggleSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectModel.objects.all()

    def perform_update(self, serializer):
        serializer.instance.is_active=not(serializer.instance.is_active)
        serializer.save()

class ProjectCreate(generics.ListCreateAPIView):
    serializer_class = ProjectCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectModel.objects.all()

    def perform_create(self, serializer):
        serializer.save()
class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectModel.objects.all()


class Service(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ServiceSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceModel.objects.filter(is_active=True).order_by('number')

class ServiceToggleArchive(generics.UpdateAPIView):
    '''Toggle Archive'''
    serializer_class = ServiceToggleSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceModel.objects.all()

    def perform_update(self, serializer):
        serializer.instance.is_active=not(serializer.instance.is_active)
        serializer.save()

class ServiceYear(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ServiceSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return ServiceModel.objects.filter(is_active=True, created__year=year).order_by('-number')
class ServiceArchive(generics.ListAPIView):
    '''Employee view'''
    serializer_class = ServiceSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return ServiceModel.objects.filter(is_active=False, created__year=year).order_by('-number')
class ServiceCreate(generics.ListCreateAPIView):
    serializer_class = ServiceCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceModel.objects.all()

    def perform_create(self, serializer):
        serializer.save()
class ServiceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceModel.objects.all()

class HSE(generics.ListAPIView):
    '''Employee view'''
    serializer_class = HSESerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HSEModel.objects.filter(is_active=True).order_by('-number')

class HSEArchive(generics.ListAPIView):
    '''Employee view'''
    serializer_class = HSESerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return HSEModel.objects.filter(is_active=False, created__year=year).order_by('-number')

class HSEToggleArchive(generics.UpdateAPIView):
    '''Toggle Archive'''
    serializer_class = HSEToggleSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HSEModel.objects.all()

    def perform_update(self, serializer):
        serializer.instance.is_active=not(serializer.instance.is_active)
        serializer.save()

class HSEYear(generics.ListAPIView):
    '''Employee view'''
    serializer_class = HSESerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return HSEModel.objects.filter(is_active=True, created__year=year).order_by('-number')

class HSECreate(generics.ListCreateAPIView):
    serializer_class = HSECreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HSEModel.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class HSERetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HSECreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HSEModel.objects.all()
@csrf_exempt
def NextProjectNumber(request):
    '''Get the Next Project, Service, and HSE Numbers'''
    year = time.strftime("%Y")[2:]
    if request.method == 'GET':
        #! what if its not sequential and we manually enter old quote or database is empty??
        #! project number
        try:
            if ProjectModel.objects.count() > 0:
                projects = list(ProjectModel.objects.filter(is_active=True).values_list('number', flat=True))

                project_list_year=[]

                for i in projects:
                    if i[-2:] == year:
                        project_list_year.append(int(i))

                if len(project_list_year):
                    last_project_number = f'{sorted(project_list_year)[-1]}'
                else:
                    raise AttributeError
            else:
                last_project = model_to_dict(ProjectModel.objects.filter(is_active=True).order_by('-number').first())
                last_project_number = (last_project['number'])

            current_project_year = last_project_number[-2:]

            if current_project_year == year:
                next_project_number = int(last_project_number[:3])+1
                next_project_number_str = f'{next_project_number}{current_project_year}'
            else:
                next_project_number = '100'
                next_project_number_str = f'{next_project_number}{year}'

        except AttributeError:
            #if database is empty
            # last_project = None  #Doesn't exist, set to None
            next_project_number_str = f'100{year}'

        #! service number
        try:
            if not ServiceModel.objects.count() > 0:
                services = list(ServiceModel.objects.filter(is_active=True).values_list('number', flat=True))

                service_list_year=[]

                for i in services:
                    if i[3:5] == year:
                        service_list_year.append(i)

                if len(service_list_year):
                    last_service_number = f'{sorted(service_list_year)[-1]}'
                else:
                    raise AttributeError

            else:
                last_service = model_to_dict(ServiceModel.objects.filter(is_active=True).order_by('-number').first())
                last_service_number = (last_service['number'])

            current_service_year = last_service_number[3:5]

            if current_service_year == year:
                next_service_number = int(last_service_number[-3:])+1
                if len(str(next_service_number)) == 1:
                    next_service_number_str = f'SVC{str(current_service_year)}00{str(next_service_number)}'
                elif len(str(next_service_number)) == 2:
                    next_service_number_str = f'SVC{str(current_service_year)}0{str(next_service_number)}'
                elif len(str(next_service_number)) == 3:
                    next_service_number_str = f'SVC{str(current_service_year)}{str(next_service_number)}'
            else:
                next_service_number = '001'
                next_service_number_str = f'SVC{year}{str(next_service_number)}'

        except AttributeError:
            #if database is empty
            last_service_number = None
            next_service_number_str = f'SVC{year}001'

        #! hse number
        try:
            if HSEModel.objects.count() > 0:
                hses = list(HSEModel.objects.filter(is_active=True).values_list('number', flat=True))

                hse_list_year=[]

                for i in hses:
                    if i[3:5] == year:
                        hse_list_year.append(i)

                if len(hse_list_year):
                    last_hse_number = f'{sorted(hse_list_year)[-1]}'
                else:
                    raise AttributeError

            else:
                last_hse = model_to_dict(HSEModel.objects.filter(is_active=True).order_by('-number').first())
                last_hse_number = (last_hse['number'])

            current_hse_year = last_hse_number[3:5]

            if current_hse_year == year:
                next_hse_number = int(last_hse_number[-2:])+1
                if len(str(next_hse_number)) == 1:
                    next_hse_number_str = f'HSE{current_hse_year}0{next_hse_number}'
                elif len(str(next_hse_number)) == 2:
                    next_hse_number_str = f'HSE{current_hse_year}{next_hse_number}'
            else:
                last_hse_number = '01'
                next_hse_number_str = f'HSE{year}{next_hse_number}'

        except AttributeError:
            #if database is empty
            last_hse_number = None
            next_hse_number_str = f'HSE{year}01'

        return JsonResponse({
            'next_project_number': str(next_project_number_str),
            'next_service_number': str(next_service_number_str),
            'next_hse_number': str(next_hse_number_str),
            }, status=201)

@csrf_exempt
def LastProject(request):
    '''Get the Last Project Number'''
    if request.method == 'GET':
        try:
            project_model = ProjectModel.objects.filter(is_active=True).order_by('-created').exists()
            if project_model:
                last_project = model_to_dict(ProjectModel.objects.filter(is_active=True).order_by('-created').first())
                last_project_id = (last_project['id'])
            else:
                last_project_id = 'Table Empty'

            service_model = ServiceModel.objects.filter(is_active=True).order_by('-created').exists()
            if service_model:
                last_service = model_to_dict(ServiceModel.objects.filter(is_active=True).order_by('-created').first())
                last_service_id = (last_service['id'])
            else:
                last_service_id = 'Table Empty'

            hse_model = HSEModel.objects.filter(is_active=True).order_by('-created').exists()
            if hse_model:
                last_hse = model_to_dict(HSEModel.objects.filter(is_active=True).order_by('-created').first())
                last_hse_id = (last_hse['id'])
            else:
                last_hse_id = 'Table Empty'

            return JsonResponse({
                'last_project_id': str(last_project_id),
                'last_service_id': str(last_service_id),
                'last_hse_id': str(last_hse_id),
                }, status=201)
        #to be more specific you can except ProfileObjectDoesNotExist
        except AttributeError:
            last_project = None  #Doesn't exist, set to None
            last_service = None  #Doesn't exist, set to None
            last_hse = None  #Doesn't exist, set to None
            return JsonResponse({
                'last_project_id': str('Table Empty'),
                'last_service_id': str('Table Empty'),
                'last_hse_id': str('Table Empty')
                }, status=201)