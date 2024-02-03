from rest_framework import serializers
from project.models import Project, ProjectCategory, ProjectType
from project.models import BillingType, OrderType
from project.models import Service, HSE

class  ProjectCategorySerializer(serializers.ModelSerializer):
    '''Project Category serializer'''
    class Meta:
        model = ProjectCategory
        fields = '__all__'

class  ProjectTypeSerializer(serializers.ModelSerializer):
    '''Project Type serializer'''
    class Meta:
        model = ProjectType
        fields = '__all__'

class  BillingTypeSerializer(serializers.ModelSerializer):
    '''Project Type serializer'''
    class Meta:
        model = BillingType
        fields = '__all__'

class  OrderTypeSerializer(serializers.ModelSerializer):
    '''Project Type serializer'''
    class Meta:
        model = OrderType
        fields = '__all__'

class  ProjectSerializer(serializers.ModelSerializer):
    '''Project serializer'''
    class Meta:
        model = Project
        fields = '__all__'
        depth = 3

class ProjectToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id']
        read_only_fields = ['number', 'name']

class MinimalProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # fields = ['id', 'number', 'name', 'is_active' ]
        fields = ['id', 'number', 'name', 'project_category', 'project_type', 'address', 'prevailing_rate']
        depth = 2
        
class ProjectCreateSerializer(serializers.ModelSerializer):
    ''' Create Project serializer'''
    is_active = serializers.BooleanField(initial=True)
    class Meta:
        model = Project
        fields = '__all__'

class  ServiceSerializer(serializers.ModelSerializer):
    '''Service serializer'''
    class Meta:
        model = Service
        fields = '__all__'
        depth = 3

class ServiceToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id']
        read_only_fields = ['number', 'name']

class MinimalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'number', 'name', 'is_active' ]

class ServiceCreateSerializer(serializers.ModelSerializer):
    ''' Create Service serializer'''
    is_active = serializers.BooleanField(initial=True)
    class Meta:
        model = Service
        fields = '__all__'

class  HSESerializer(serializers.ModelSerializer):
    '''HSE serializer'''
    class Meta:
        model = HSE
        fields = '__all__'
        depth = 3

class HSEToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSE
        fields = ['id']
        read_only_fields = ['number', 'name']

class MinimalHSESerializer(serializers.ModelSerializer):
    class Meta:
        model = HSE
        fields = ['id', 'number', 'name', 'is_active' ]

class HSECreateSerializer(serializers.ModelSerializer):
    ''' Create HSE serializer'''
    is_active = serializers.BooleanField(initial=True)
    class Meta:
        model = HSE
        fields = '__all__'