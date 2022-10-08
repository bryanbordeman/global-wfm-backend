from email.policy import default
from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User

class Quote(models.Model):
    is_active = models.BooleanField(null= False, default=True)
    number = models.CharField(max_length=8, null= True)
    name = models.CharField(max_length=200, null= True)
    due = models.DateField(null=False)
    project_category = models.ForeignKey('project.ProjectCategory', on_delete=models.SET_NULL, null=True)
    project_type = models.ForeignKey('project.ProjectType', on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey('contact.Address', null=True, blank=True, on_delete=models.PROTECT)
    customers = models.ManyToManyField('contact.Company', blank=True)
    prevailing_rate = models.BooleanField(null= False, default=False)
    travel_job = models.BooleanField(null= False, default=False)
    price = models.FloatField(null=True, blank=True, default=0)
    revision = models.IntegerField(null=True, default=0)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])

    def __str__(self):
        return self.number

