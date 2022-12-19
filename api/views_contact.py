from rest_framework import generics, permissions
from .serializers_contact import ContactSerializer
from contact.models import Contact as ContactModel

class Contact(generics.ListAPIView):
    '''Contact view'''
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContactModel.objects.all()

class ContactQuote(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        quote = self.kwargs['quote_id']
        return ContactModel.objects.filter(quotes=quote).all()

#! Make ContactProject
class ContactProject(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = self.kwargs['project_id']
        return ContactModel.objects.filter(projects=project).all()

class ContactService(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service = self.kwargs['service_id']
        return ContactModel.objects.filter(services=service).all()

class ContactHSE(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hse = self.kwargs['hse_id']
        return ContactModel.objects.filter(hses=hse).all()

class ContactCompany(generics.ListAPIView):
    '''get all worksegments for particular isoweek. Admin view only'''
    serializer_class = ContactSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        company = self.kwargs['company_id']
        return ContactModel.objects.filter(company=company).all()


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