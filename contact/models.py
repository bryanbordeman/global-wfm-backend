from django.db import models
from django_countries.fields import CountryField
from localflavor.us.models import USZipCodeField, USStateField
from phone_field import PhoneField

class Address(models.Model):
    place_id = models.CharField("Place ID", max_length=1024,)
    address = models.CharField("Address line 1", max_length=1024,)
    city = models.CharField( "City", max_length=1024,)
    state = models.CharField(max_length=200, null= True)
    postal_code = USZipCodeField()
    country = CountryField()

    def __str__(self):
        return f'''{self.address}, {self.city}, {self.state} {self.postal_code}'''

class Phone(models.Model):
    TYPE = (
        ('Mobile', 'Mobile'),
        ('Main', 'Main'),
        ('Work','Work'),
        ('Home','Home'),
        ('Direct','Direct'),
        ('Fax','Fax'),
    )
    phone_number = PhoneField(blank=True) # validators should be a list
    phone_type = models.CharField(max_length=200, null=True, choices=TYPE, default=TYPE[0][0])

    def __str__(self):
        return f'{self.phone_number} {self.phone_type}'

class Company(models.Model):
    name = models.CharField(max_length=100, null= True)
    # address = models.ManyToManyField(Address, blank=True)
    phone = models.ManyToManyField(Phone, blank=True)
    fax = models.ForeignKey(Phone, related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    website = models.URLField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=200, null= True)
    job_title = models.CharField(max_length=200, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.PROTECT)
    address = models.ForeignKey('contact.Address', null=True, blank=True, on_delete=models.PROTECT)
    phone = models.ManyToManyField(Phone, blank=True)
    fax = models.ForeignKey(Phone, related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(max_length=200, null= True, blank=True)
    quotes = models.ManyToManyField('quote.Quote', blank=True)
    projects = models.ManyToManyField('project.Project', blank=True)

    def __str__(self):
        return self.name