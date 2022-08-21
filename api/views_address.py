from rest_framework import generics, permissions
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
        serializer.save()

class AddressRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AddressModel.objects.all()