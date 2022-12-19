from django.contrib import admin
from .models import WorkSegment, WorkType

# Register your models here.
admin.site.register(WorkSegment)
admin.site.register(WorkType)