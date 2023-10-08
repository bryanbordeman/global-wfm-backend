from rest_framework import generics, permissions
from .serializers_engineering import DCNSerializer, DCNCreateSerializer
from engineering.models import DCN as DCNModel

class DCNViewset(generics.ListAPIView):
    '''Contact view'''
    serializer_class = DCNSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs['year']
        return DCNModel.objects.filter(created__year=year).order_by('-number')

class DCNCreate(generics.ListCreateAPIView):
    serializer_class = DCNCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DCNModel.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class DCNRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DCNCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DCNModel.objects.all()

    def perform_update(self, serializer):
        serializer.save()
