from django.contrib import admin
from .models import ProjectCategory, ProjectType
from .models import Project, Service, HSE
from .models import OrderType, BillingType

admin.site.register(ProjectCategory)
admin.site.register(ProjectType)
admin.site.register(BillingType)
admin.site.register(OrderType)
admin.site.register(Project)
admin.site.register(Service)
admin.site.register(HSE)
