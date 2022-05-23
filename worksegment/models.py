from cgi import print_form
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from datetime import date, datetime
from isoweek import Week

# validators
def no_future(value):
    '''checks date is not in future'''
    today = date.today()
    if value > today:
        raise ValidationError('Date cannot be in the future.')

# Create your models here.
class WorkSegment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.CharField(max_length=10, null=True, blank=True)
    is_approved = models.BooleanField(null= False, default=False)
    date = models.DateField(null=True, validators=[no_future])
    isoweek = models.CharField(max_length=8, blank=True, editable=False)
    start_time = models.TimeField(null=True, blank=False)
    end_time = models.TimeField(null=True, blank=False)
    lunch = models.BooleanField(null= False, default=True)
    travel_duration = models.DecimalField(max_digits= 5, decimal_places = 2, null=True, blank=True, default=0)
    duration = models.DecimalField(max_digits= 5, decimal_places = 2, null=True, blank=True, default=0, editable=False)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])

    def clean(self):
        '''checks end time is greater than start time'''
        if self.start_time > self.end_time:
            raise ValidationError('Start time needs to be before end time')
        return super().clean()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lte = models.F('end_time')),
                name='start_before_end'
            )
        ]
    
    def __str__(self):
        return f'User: {self.user} | Week: {self.isoweek} | Project: {self.project} | Date: {self.date} | Id: {self.id}'

    def save(self, *args, **kwargs):
        'get delta between end and start time and save to duration as float'
        delta = datetime.combine(self.date, self.end_time) - datetime.combine(self.date, self.start_time)
        if self.lunch:
            self.duration = (round(delta.total_seconds()/60)/60) - 0.5
        else:
            self.duration = (round(delta.total_seconds()/60)/60)

        'convert date to isoweek'
        self.isoweek = Week.withdate(self.date)

        super(WorkSegment, self).save(*args, **kwargs)