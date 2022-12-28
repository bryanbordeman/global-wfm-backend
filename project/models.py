from django.db import models
from django.core.validators import MaxLengthValidator

class ProjectCategory(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class ProjectType(models.Model):
    project_category = models.ManyToManyField(ProjectCategory, blank=True)
    # project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class BillingType(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name
class OrderType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class BaseProject(models.Model):
    is_active = models.BooleanField(null= False, default=True)
    number = models.CharField(max_length=8, null= True)
    name = models.CharField(max_length=200, null= True)
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('contact.Address', null=True, blank=True, on_delete=models.PROTECT)
    customer = models.ForeignKey('contact.Company', on_delete=models.PROTECT)
    terms = models.CharField(max_length=200, null= True)
    prevailing_rate = models.BooleanField(null= False, default=False)
    union = models.BooleanField(null= False, default=False)
    certified_payroll = models.BooleanField(null= False, default=False)
    material_only = models.BooleanField(null= False, default=False)
    travel_job = models.BooleanField(null= False, default=False)
    tax_exempt = models.BooleanField(null= False, default=False)
    billing_type = models.ForeignKey(BillingType, on_delete=models.SET_NULL, null=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(null=True, blank=True, default=0)
    po_number = models.CharField(max_length=200, blank=True)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    created = models.DateField(auto_now_add=True)
    class Meta:
        abstract = True
        
class Project(BaseProject):
    def __str__(self):
        return f'{self.number} {self.name}'

class Service(BaseProject):
    def __str__(self):  
        return f'{self.number} {self.name}'

class HSE(BaseProject):
    def __str__(self):
        return f'{self.number} {self.name}'