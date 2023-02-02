from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Holiday)
admin.site.register(VehicleIssue)
admin.site.register(VehicleCleaning)
admin.site.register(VehicleService)
admin.site.register(VehicleInspection)
admin.site.register(Vehicle)
admin.site.register(Travel)
admin.site.register(ScheduleSegment)
admin.site.register(Schedule)
