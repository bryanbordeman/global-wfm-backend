from django.contrib import admin
from .models import ProjectCategory, ProjectType, BillingType, OrderType, Project

admin.site.register(ProjectCategory)
admin.site.register(ProjectType)
admin.site.register(BillingType)
admin.site.register(OrderType)
admin.site.register(Project)