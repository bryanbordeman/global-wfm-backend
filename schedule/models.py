from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Holiday(models.Model):
    CHOICES = (('New Years Day','New Years Day'),
                ('Memorial Day','Memorial Day'),
                ('Independence Day','Independence Day'),
                ('Labor Day','Labor Day'),
                ('Thanksgiving Day','Thanksgiving Day'),
                ('Friday after Thanksgiving','Friday after Thanksgiving'),
                ('Christmas Eve','Christmas Eve'),
                ('Christmas Day','Christmas Day'),
                ('Good Friday', 'Good Friday'),
                ('New Years Eve','New Years Eve'),)

    is_observed = models.BooleanField(null= False, default=False)
    holiday = models.CharField(max_length=200, null=True, choices=CHOICES)
    date = models.DateField(null=True)
    paid_employee = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.holiday}-{self.date}'

class VehicleCleaning(models.Model):
    date = models.DateField(null=True)
    wash_exterior = models.BooleanField(null= False, default=False)
    wash_interior = models.BooleanField(null= False, default=False)
    clean_windows = models.BooleanField(null= False, default=False)
    wash_seats = models.BooleanField(null= False, default=False)
    vacuum_seats = models.BooleanField(null= False, default=False)
    vacuum_floor = models.BooleanField(null= False, default=False)
    other = models.BooleanField(null= False, default=False)
    other_description = models.CharField(max_length=500, blank=True)

class VehicleService(models.Model):
    description = models.CharField(max_length=500, blank=True)
    date = models.DateField(null=True)

class VehicleInspection(models.Model):
    description = models.CharField(max_length=500, blank=True)
    date = models.DateField(null=True)

class Vehicle(models.Model):
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=4, blank=True)
    color = models.CharField(max_length=50, blank=True)
    license_plate = models.CharField(max_length=50, blank=True)
    nickname = models.CharField(max_length=50)
    cleanings = models.ManyToManyField(VehicleCleaning, blank=True,)
    services = models.ManyToManyField(VehicleService, blank=True,)
    inspections = models.ManyToManyField(VehicleService, blank=True,)
    assignment = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    max_passagers = models.IntegerField(default=0)
    max_weight = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        
        return f'{self.nickname}'

class Travel(models.Model):
    hotel = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    flight = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    car_rental = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])

class ScheduleSegment(models.Model):
    users = models.ManyToManyField(User, blank=True,)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.PROTECT)
    # date = models.DateField(null=True)
    start_time = models.TimeField(null=True, blank=False)
    end_time = models.TimeField(null=True, blank=False)
    scope = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    is_travel = models.BooleanField(null= False, default=False)
    travel = models.ForeignKey(Travel, null=True, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        local_or_travel = 'L'
        if self.is_travel:
            local_or_travel = 'T'

        return f'{self.project}-{local_or_travel} | {self.vehicle.make} {self.vehicle.model}'

class Schedule(models.Model):
    segments= models.ManyToManyField(ScheduleSegment, blank=True)
    date = models.DateField(null=True)
    isoday = models.CharField(max_length=8, blank=True, editable=False)
    isoweek = models.CharField(max_length=8, blank=True, editable=False)

    def __str__(self):
        return f'{self.isoday} | {self.isoweek}'

