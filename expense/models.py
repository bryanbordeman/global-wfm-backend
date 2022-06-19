from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from datetime import date
from django.core.exceptions import ValidationError
from imagekit.models.fields import ProcessedImageField

# validators
def no_future(value):
    '''checks date is not in future'''
    today = date.today()
    if value > today:
        raise ValidationError('Expense was not created. Date cannot be in the future.')

class MileRate (models.Model):
    rate = models.FloatField(null= True)
    year = models.IntegerField(null=False)

    def __str__(self):
        return f'$ {self.rate} | {self.year} Rate'

class Mile (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.CASCADE)
    miles = models.FloatField(null= True)
    rate = models.ForeignKey(MileRate, null=True, on_delete=models.SET_NULL)
    price = models.FloatField(null= True)
    notes = models.TextField(max_length=250, blank=True,
                            validators=[MaxLengthValidator(250)])
    is_approved = models.BooleanField(null= False, default=False)
    date = models.DateField(null=True, validators=[no_future])
    date_created = models.DateField(auto_now_add= True)

    @property
    def price(self):
        return round(self.miles * self.rate.rate, 2)

    def __str__(self):
        return f'{self.user.username}_{self.project}_${self.price}_{self.date_created}'

class Expense (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', null=True, on_delete=models.CASCADE)
    receipt_pic = ProcessedImageField(default='receipt.png', format='JPEG', upload_to='None', options={'quality': 20})
    merchant = models.CharField(max_length=200, null= True, blank=True)
    price = models.FloatField(null= True)
    notes = models.TextField(max_length=250, blank=True,
                            validators=[MaxLengthValidator(250)])
    is_reimbursable = models.BooleanField(null= False, default=False)
    is_approved = models.BooleanField(null= False, default=False)
    date_purchased = models.DateField(null=True, validators=[no_future])
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.user.username}_{self.project}_{self.merchant}_{self.date_purchased}'
