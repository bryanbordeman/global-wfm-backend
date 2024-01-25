from django.contrib import admin
from .models import Employee
from .models import EmployeeRate

admin.site.register(Employee)
admin.site.register(EmployeeRate)