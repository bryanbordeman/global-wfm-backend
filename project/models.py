from django.db import models
from django.core.validators import MaxLengthValidator

class ProjectCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ProjectType(models.Model):
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Project(models.Model):
    is_active = models.BooleanField(null= False, default=True)
    number = models.CharField(max_length=8, null= True)
    name = models.CharField(max_length=200, null= True)
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('contact.Address', null=True, blank=True, on_delete=models.PROTECT)
    customer_company = models.ForeignKey('contact.Company', null=True, blank=True, on_delete=models.PROTECT)
    contact = models.ManyToManyField('contact.Contact', blank=True)
    prevailing_rate = models.BooleanField(null= False, default=False)
    travel_job = models.BooleanField(null= False, default=False)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])

    def __str__(self):
        return self.number
