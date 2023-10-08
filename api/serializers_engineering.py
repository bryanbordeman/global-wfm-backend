from dataclasses import field
from rest_framework import serializers
from engineering.models import DCN
from api.serializers_user import MinimalUserSerializer
from api.serializers_project import MinimalProjectSerializer
from api.serializers_project import MinimalServiceSerializer
from api.serializers_project import MinimalHSESerializer
from api.serializers_quote import MinimalQuoteSerializer

class  DCNSerializer(serializers.ModelSerializer):
    '''Task serializer'''
    created_by = MinimalUserSerializer()
    project = MinimalProjectSerializer()
    service = MinimalServiceSerializer()
    hse = MinimalHSESerializer()
    quote = MinimalQuoteSerializer()
    
    class Meta:
        model = DCN
        fields = '__all__'
        depth = 1

class  DCNCreateSerializer(serializers.ModelSerializer):
    '''Create Task serializer'''
    class Meta:
        model = DCN
        fields = '__all__'