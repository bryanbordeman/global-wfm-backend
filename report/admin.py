from django.contrib import admin
from .models import ProjectReport, DoorServiceReport, IncidentReport

admin.site.register(ProjectReport)
admin.site.register(DoorServiceReport)
admin.site.register(IncidentReport)
