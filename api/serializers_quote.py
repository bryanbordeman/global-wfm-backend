from rest_framework import serializers
from quote.models import Quote
from api.serializers_user import MinimalUserSerializer

class QuoteSerializer(serializers.ModelSerializer):
    '''Project serializer'''
    manager = MinimalUserSerializer()
    class Meta:
        model = Quote
        fields = '__all__'
        depth = 3

class QuoteToggleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id']
        read_only_fields = ['number', 'name']
class MinimalQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'number', 'name', 'is_active' ]

class QuoteCreateSerializer(serializers.ModelSerializer):
    ''' Create Project serializer'''
    is_active = serializers.BooleanField(initial=True)
    class Meta:
        model = Quote
        fields = '__all__'