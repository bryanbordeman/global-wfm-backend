from rest_framework import serializers
from report.models import ProjectReport, DoorServiceReport, IncidentReport

class ProjectReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectReport
        fields = '__all__'
        depth = 1

class ProjectReportCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectReport
        fields = '__all__'

class DoorServiceReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoorServiceReport
        fields = '__all__'
        depth = 1

class DoorServiceReportCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoorServiceReport
        fields = '__all__'

class IncidentReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncidentReport
        fields = '__all__'
        depth = 1

class IncidentReportCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncidentReport
        fields = '__all__'