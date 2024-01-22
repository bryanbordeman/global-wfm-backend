from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_salary = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    documents = models.ManyToManyField('uploader.DropBox', blank=True) # attachments are only images for now.

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'