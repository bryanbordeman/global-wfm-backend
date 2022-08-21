from rest_framework import generics, permissions
from .serializers_contact import ContactSerializer
from contact.models import Contact as ContactModel

class Contact(generics.ListAPIView):
    '''Contact view'''
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContactModel.objects.all()

class ContactCreate(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContactModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class ContactRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContactModel.objects.all()