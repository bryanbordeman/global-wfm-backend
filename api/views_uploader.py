from rest_framework import generics, permissions
from uploader.models import DropBox
from uploader.models import Drawing
from uploader.models import DrawingType
from .serializers_uploader import DropBoxSerializer
from .serializers_uploader import DrawingSerializer
from .serializers_uploader import DrawingTypeSerializer

class DropBoxViewset(generics.ListAPIView):

    serializer_class = DropBoxSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DropBox.objects.all()

class DropBoxCreate(generics.ListCreateAPIView):
    serializer_class = DropBoxSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DropBox.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DropBoxRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DropBoxSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DropBox.objects.all()
    

class DrawingViewset(generics.ListAPIView):

    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Drawing.objects.all()
    
class DrawingProject(generics.ListAPIView):

    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Drawing.objects.filter(project_id=project_id, is_active=True).all()

class DrawingService(generics.ListAPIView):

    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return Drawing.objects.filter(service_id=service_id, is_active=True).all()

class DrawingHSE(generics.ListAPIView):

    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hse_id = self.kwargs['hse_id']
        return Drawing.objects.filter(hse_id=hse_id, is_active=True).all()

class DrawingCreate(generics.ListCreateAPIView):
    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Drawing.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DrawingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrawingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Drawing.objects.all()
    
class DrawingTypeView(generics.ListAPIView):

    serializer_class = DrawingTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DrawingType.objects.all()
    
class DrawingTypeCreate(generics.ListCreateAPIView):
    serializer_class = DrawingTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DrawingType.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DrawingTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrawingTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DrawingType.objects.all()