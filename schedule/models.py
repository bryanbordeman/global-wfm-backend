from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from imagekit.models.fields import ProcessedImageField
from isoweek import Week
from django.core.exceptions import ValidationError

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

class Vehicle(models.Model):
    image = ProcessedImageField(default='van.png', format='JPEG', upload_to='None', options={'quality': 20})
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=4, blank=True)
    color = models.CharField(max_length=50, blank=True)
    license_plate = models.CharField(max_length=50, blank=True)
    nickname = models.CharField(max_length=50)
    assignment = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    max_passagers = models.IntegerField(default=0)
    max_weight = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):

        return f'{self.nickname}'

class VehicleCleaning(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.PROTECT)
    date = models.DateField(null=True)
    wash_exterior = models.BooleanField(null= False, default=False)
    wash_interior = models.BooleanField(null= False, default=False)
    clean_windows = models.BooleanField(null= False, default=False)
    wash_seats = models.BooleanField(null= False, default=False)
    vacuum_seats = models.BooleanField(null= False, default=False)
    vacuum_floor = models.BooleanField(null= False, default=False)
    other = models.BooleanField(null= False, default=False)
    other_description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.vehicle.nickname} | {self.date}'

class VehicleIssue(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.PROTECT)
    description = models.CharField(max_length=500, blank=True)
    date = models.DateField(null=True, auto_now_add=True)
    is_resolved = models.BooleanField(null= False, default=False)

    def __str__(self):
        return f'{self.vehicle.nickname} | {self.date}'

class VehicleService(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.PROTECT)
    description = models.CharField(max_length=500, blank=True)
    date = models.DateField(null=True)

    def __str__(self):
        return f'{self.vehicle.nickname} | {self.date}'

class VehicleInspection(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, null=True, on_delete=models.PROTECT)
    description = models.CharField(max_length=500, blank=True)
    expiration_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.vehicle.nickname} | {self.expiration_date}'

class Travel(models.Model):
    hotel = models.TextField(max_length=4000, blank=True,
                                validators=[MaxLengthValidator(4000)])
    flight = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(4000)])
    car_rental = models.TextField(max_length=4000, blank=True,
                                validators=[MaxLengthValidator(4000)])

class ProjectSegment(models.Model):
    quote = models.ForeignKey('quote.Quote', null=True, blank=True, on_delete=models.PROTECT)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    service = models.ForeignKey('project.Service', null=True, blank=True, on_delete=models.PROTECT)
    hse = models.ForeignKey('project.HSE', null=True, blank=True, on_delete=models.PROTECT)
    user = models.ManyToManyField(User, related_name='employees')
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

class WeekSegment(models.Model):
    isoweek = models.CharField(max_length=8, blank=True, editable=False)
    date = models.DateField(null=True)

    def add_day(self, day):
        if self.days.count() < 7:
            self.days.add(day)
        else:
            raise ValidationError('A WeekSegment cannot have more than 7 DaySegments')
        
    def save(self, *args, **kwargs):
        if self.date:
            self.isoweek = self.date.isocalendar()[1]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.isoweek}'

class DaySegment(models.Model):
    date = models.DateField(null=True)
    isoday = models.CharField(max_length=8, blank=True, editable=False)
    week_segment = models.ForeignKey(WeekSegment, related_name='days', on_delete=models.CASCADE)
    project_segments = models.ManyToManyField(ProjectSegment) 

    def __str__(self):
        return f'{self.isoday}'

    def save(self, *args, **kwargs):
        if self.date:
            self.isoday = self.date.isocalendar()[2]
        self.week_segment.add_day(self)
        super().save(*args, **kwargs)

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