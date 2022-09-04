from rest_framework import generics, permissions
from rest_framework.response import Response
from django.core import serializers
from .serializers_contact import AddressSerializer
from contact.models import Address as AddressModel

class Address(generics.ListAPIView):
    '''Address view'''
    serializer_class = AddressSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AddressModel.objects.all()

class AddressCreate(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AddressModel.objects.all()
    
    def perform_create(self, serializer):
        # place_id = serializer.data['place_id']
        # exist = AddressModel.objects.filter(place_id=place_id).exists()
        # if exist:
        #     existing_instance = AddressModel.objects.filter(place_id=place_id)
        #     data = serializers.serialize("json", existing_instance)
        #     print(data)
        # else:
        #     return Response(serializer.data)
        serializer.save()

class AddressRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AddressModel.objects.all()