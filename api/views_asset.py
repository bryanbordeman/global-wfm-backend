from rest_framework import generics, permissions
from django.utils.timezone import now

from asset.models import (
    DoorReport,
    DoorRev,
    DoorLockset,
    DoorType,
    DoorSillType,
    DoorFrameType,
    DoorCoreType,
    DoorHingeType,
    DoorOptions,
    DoorPackaging,
    Door,
)
from .serializers_asset import (
    DoorReportSerializer,
    DoorRevSerializer,
    DoorRevCreateSerializer,
    DoorLocksetSerializer,
    DoorTypeSerializer,
    DoorSillTypeSerializer,
    DoorFrameTypeSerializer,
    DoorCoreTypeSerializer,
    DoorHingeTypeSerializer,
    DoorOptionsSerializer,
    DoorPackagingSerializer,
    DoorSerializer,
    DoorCreateSerializer,
    MinimalDoorSerializer,
    DoorCompletedSerializer,
)



class DoorReportViewset(generics.ListAPIView):

    serializer_class = DoorReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorReport.objects.all()

class DoorReportCreate(generics.ListCreateAPIView):
    serializer_class = DoorReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorReport.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorReportRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorReportSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorReport.objects.all()

class DoorRevViewset(generics.ListAPIView):

    serializer_class = DoorRevSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorRev.objects.all()

class DoorRevCreate(generics.ListCreateAPIView):
    serializer_class = DoorRevCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorRev.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorRevRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorRevSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorRev.objects.all()

class DoorLocksetViewset(generics.ListAPIView):

    serializer_class = DoorLocksetSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorLockset.objects.all()

class DoorLocksetCreate(generics.ListCreateAPIView):
    serializer_class = DoorLocksetSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorLockset.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorLocksetRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorLocksetSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorLockset.objects.all()

class DoorTypeViewset(generics.ListAPIView):

    serializer_class = DoorTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorType.objects.all()

class DoorTypeCreate(generics.ListCreateAPIView):
    serializer_class = DoorTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorType.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorType.objects.all()

class DoorSillTypeViewset(generics.ListAPIView):

    serializer_class = DoorSillTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorSillType.objects.all()

class DoorSillTypeCreate(generics.ListCreateAPIView):
    serializer_class = DoorSillTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorSillType.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorSillTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorSillTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorSillType.objects.all()

class DoorFrameTypeViewset(generics.ListAPIView):

    serializer_class = DoorFrameTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorFrameType.objects.all()

class DoorFrameTypeCreate(generics.ListCreateAPIView):
    serializer_class = DoorFrameTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorFrameType.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorFrameTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorFrameTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorFrameType.objects.all()

class DoorCoreTypeViewset(generics.ListAPIView):

    serializer_class = DoorCoreTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorCoreType.objects.all()

class DoorCoreTypeCreate(generics.ListCreateAPIView):
    serializer_class = DoorCoreTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorCoreType.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorCoreTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorCoreTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorCoreType.objects.all()

class DoorHingeTypeViewset(generics.ListAPIView):

    serializer_class = DoorHingeTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorHingeType.objects.all()

class DoorHingeTypeCreate(generics.ListCreateAPIView):
    serializer_class = DoorHingeTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorHingeType.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorHingeTypeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorHingeTypeSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorHingeType.objects.all()

class DoorOptionsViewset(generics.ListAPIView):

    serializer_class = DoorOptionsSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorOptions.objects.all()

class DoorOptionsCreate(generics.ListCreateAPIView):
    serializer_class = DoorOptionsSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorOptions.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorOptionsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorOptionsSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorOptions.objects.all()

class DoorPackagingViewset(generics.ListAPIView):

    serializer_class = DoorPackagingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorPackaging.objects.all()

class DoorPackagingCreate(generics.ListCreateAPIView):
    serializer_class = DoorPackagingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorPackaging.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorPackagingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorPackagingSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoorPackaging.objects.all()

class DoorViewset(generics.ListAPIView):

    serializer_class = MinimalDoorSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Door.objects.filter(is_complete=False).order_by('due')

class DoorCreate(generics.ListCreateAPIView):
    serializer_class = DoorCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Door.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DoorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoorCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Door.objects.all()

class DoorRetrieve(generics.RetrieveAPIView):
    serializer_class = MinimalDoorSerializer
    permission_classes = []  # Remove the authentication requirement

    def get_queryset(self):
        return Door.objects.all()

class DoorToggleCompleted(generics.UpdateAPIView):
    '''Complete Door'''
    serializer_class = DoorCompletedSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Door.objects.all()

    def perform_update(self, serializer):
        serializer.instance.is_complete=not(serializer.instance.is_complete)
        serializer.instance.completed=(now())
        serializer.save()

class DoorProjectList(generics.ListAPIView):
    '''Get all doors on a project'''
    serializer_class = DoorSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = self.kwargs['project']
        return Door.objects.filter(**{"project_id" : project}).all()

class DoorAttributesViewset(generics.ListAPIView):
    queryset = Door.objects.all()  # Replace "Door" with your actual model name
    serializer_class = DoorSerializer  # Replace with your actual serializer class

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        attributes = {
            "door_type": DoorType.objects.all().order_by('id'),
            "lockset": DoorLockset.objects.all().order_by('id'),
            "sill_type": DoorSillType.objects.all().order_by('id'),
            "frame_type": DoorFrameType.objects.all().order_by('id'),
            "core_type": DoorCoreType.objects.all().order_by('id'),
            "hinge_type": DoorHingeType.objects.all().order_by('id'),
            "options": DoorOptions.objects.all().order_by('id'),
            "packaging": DoorPackaging.objects.all().order_by('id'),
        }

        attribute_serializers = {
            "door_type": DoorTypeSerializer(attributes["door_type"], many=True),
            "lockset": DoorLocksetSerializer(attributes["lockset"], many=True),
            "sill_type": DoorSillTypeSerializer(attributes["sill_type"], many=True),
            "frame_type": DoorFrameTypeSerializer(attributes["frame_type"], many=True),
            "core_type": DoorCoreTypeSerializer(attributes["core_type"], many=True),
            "hinge_type": DoorHingeTypeSerializer(attributes["hinge_type"], many=True),
            "options": DoorOptionsSerializer(attributes["options"], many=True),
            "packaging": DoorPackagingSerializer(attributes["packaging"], many=True),
        }

        serialized_attributes = {}
        for attribute_name, serializer in attribute_serializers.items():
            serialized_attributes[attribute_name] = serializer.data

        response.data = {"attributes": serialized_attributes}

        return response

