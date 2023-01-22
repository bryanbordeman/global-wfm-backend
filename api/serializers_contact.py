from rest_framework import serializers
from contact.models import Address, Phone, Company, Contact

class AddressSerializer(serializers.ModelSerializer):
    '''Address serializer'''
    class Meta:
        model = Address
        fields = '__all__'

class PhoneSerializer(serializers.ModelSerializer):
    '''Phone serializer'''
    class Meta:
        model = Phone
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    '''Company serializer'''
    class Meta:
        model = Company
        fields = '__all__'

class CompanyShortSerializer(serializers.ModelSerializer):
    '''Company serializer'''
    class Meta:
        model = Company
        fields = ['id', 'name', 'website']

class ContactSerializer(serializers.ModelSerializer):
    '''Contact serializer'''
    class Meta:
        model = Contact
        fields = '__all__'
        depth = 2

class ContactUpdateSerializer(serializers.ModelSerializer):
    '''Update Contact serializer'''
    class Meta:
        model = Contact
        fields = '__all__'