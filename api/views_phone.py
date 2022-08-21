from rest_framework import generics, permissions
from .serializers_contact import PhoneSerializer
from contact.models import Phone as PhoneModel

class Phone(generics.ListAPIView):
    '''Phone view'''
    serializer_class = PhoneSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PhoneModel.objects.all()

class PhoneCreate(generics.ListCreateAPIView):
    serializer_class = PhoneSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PhoneModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class PhoneRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhoneSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PhoneModel.objects.all()