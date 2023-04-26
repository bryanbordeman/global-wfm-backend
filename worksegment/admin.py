from django.contrib import admin
from .models import WorkSegment, WorkType, PTO

# Register your models here.
admin.site.register(PTO)
admin.site.register(WorkSegment)
admin.site.register(WorkType)