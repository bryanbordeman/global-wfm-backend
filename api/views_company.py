from rest_framework import generics, permissions
from .serializers_contact import CompanySerializer
from contact.models import Company as CompanyModel

class Company(generics.ListAPIView):
    '''Company view'''
    serializer_class = CompanySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompanyModel.objects.all()

class CompanyCreate(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompanyModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class CompanyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompanyModel.objects.all()