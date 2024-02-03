from django.contrib import admin
from .models import Employee
from .models import EmployeeRate
from .models import PrevailingRate
from .models import Benefit
from .models import EmployeeBenefit

admin.site.register(Employee)
admin.site.register(EmployeeRate)
admin.site.register(PrevailingRate)
admin.site.register(Benefit)
admin.site.register(EmployeeBenefit)