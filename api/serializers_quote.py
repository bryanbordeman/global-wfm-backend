from rest_framework import serializers
from quote.models import Quote

class  QuoteSerializer(serializers.ModelSerializer):
    '''Project serializer'''
    class Meta:
        model = Quote
        fields = '__all__'
        depth = 3

class MinimalQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'number', 'name', 'is_active' ]

class  QuoteCreateSerializer(serializers.ModelSerializer):
    ''' Create Project serializer'''
    is_active = serializers.BooleanField(initial=True)
    class Meta:
        model = Quote
        fields = '__all__'