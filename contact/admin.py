from django.contrib import admin
from .models import Address, Phone, Company, Contact

admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(Company)
admin.site.register(Contact)