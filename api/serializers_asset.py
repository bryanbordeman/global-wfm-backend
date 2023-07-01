from rest_framework import serializers
from asset.models import DoorReport
from asset.models import DoorRev
from asset.models import DoorLockset
from asset.models import DoorType
from asset.models import DoorSillType
from asset.models import DoorFrameType
from asset.models import DoorCoreType
from asset.models import DoorHingeType
from asset.models import DoorOptions
from asset.models import DoorPackaging
from asset.models import Door

class DoorReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorReport
        fields = '__all__'

class DoorRevSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorRev
        fields = '__all__'

class DoorLocksetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorLockset
        fields = '__all__'

class DoorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorType
        fields = '__all__'

class DoorSillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorSillType
        fields = '__all__'

class DoorFrameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorFrameType
        fields = '__all__'

class DoorCoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorCoreType
        fields = '__all__'

class DoorHingeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorHingeType
        fields = '__all__'

class DoorOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorOptions
        fields = '__all__'

class DoorPackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoorPackaging
        fields = '__all__'

class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = '__all__'

        