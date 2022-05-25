from django.contrib import admin
from .models import ProjectCategory, ProjectType, Project

admin.site.register(ProjectCategory)
admin.site.register(ProjectType)
admin.site.register(Project)