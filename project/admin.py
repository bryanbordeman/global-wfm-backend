from django.contrib import admin
from .models import ProjectCategory, ProjectType, BillingType
from .models import OrderType, Project, Service, HSE

admin.site.register(ProjectCategory)
admin.site.register(ProjectType)
admin.site.register(BillingType)
admin.site.register(OrderType)
admin.site.register(Project)
admin.site.register(Service)
admin.site.register(HSE)
