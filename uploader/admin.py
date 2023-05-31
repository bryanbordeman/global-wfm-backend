from django.contrib import admin
from .models import DropBox
from .models import DrawingType
from .models import Drawing

admin.site.register(DropBox)
admin.site.register(DrawingType)
admin.site.register(Drawing)