from django.contrib import admin
from .models import *
from .models import Mile

# Register your models here.
admin.site.register(Expense)
admin.site.register(MileRate)
admin.site.register(Mile)