from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from datetime import date, datetime
import math


class Benefit(models.Model):
    description = models.CharField(max_length=200, null= True)

    def __str__(self):
        return f'{self.description}'

class EmployeeBenefit(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    employer_paid = models.BooleanField(default=False)
    effective_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.benefit.description} - {self.employee.user.first_name} {self.employee.user.last_name}{" - Employer Paid" if self.employer_paid else ""}'


class EmployeeHoursSettings(models.Model):
    sick_hours = models.DecimalField(max_digits=7, decimal_places=2, default=40)
    holiday_hours = models.DecimalField(max_digits=7, decimal_places=2, default=72)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(EmployeeHoursSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    is_salary = models.BooleanField(default=False)
    is_full_time = models.BooleanField(default=True)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    documents = models.ManyToManyField('uploader.DropBox', blank=True) # attachments are only images for now.
    vacation_hours = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    sick_hours = models.DecimalField(max_digits=7, decimal_places=2, default=EmployeeHoursSettings.load().sick_hours)
    holiday_hours = models.DecimalField(max_digits=7, decimal_places=2, default=EmployeeHoursSettings.load().holiday_hours)
    benefits = models.ManyToManyField(Benefit, through='EmployeeBenefit', blank=True)

    def years_worked(self):
        end_of_year = date(date.today().year, 12, 31)
        return (end_of_year - self.start_date).days // 365
    
    from datetime import timedelta

    def eligible_vacation_hours(self):
        years_worked = self.years_worked()
        if years_worked == 0:
            # Calculate the number of days since start_date
            days_since_start = (date.today() - self.start_date).days
            if days_since_start < 90:
                return 0
            else:
                # Determine the quarter of start_date
                quarter = (self.start_date.month - 1) // 3 + 1
                if quarter == 1:
                    return 2.5 * 8
                elif quarter == 2:
                    return 2 * 8
                elif quarter == 3:
                    return 1 * 8
                else:  # quarter == 4
                    return 0
        elif years_worked == 1:
            return 3 * 8
        elif years_worked == 2:
            return 5 * 8
        elif years_worked == 3:
            return 7 * 8
        elif years_worked == 4:
            return 8 * 8
        elif years_worked == 5:
            return 9 * 8
        elif 6 <= years_worked <= 9:
            return 10 * 8
        elif 10 <= years_worked <= 15:
            return (10 + years_worked - 9) * 8
        else:
            return (15) * 8

    def vacation_accrual_multiplier (self):
        weeks_per_year = 52
        return self.eligible_vacation_hours() / (weeks_per_year-self.week_started())
    
    def vacation_accrualed(self):
        weeks_worked = datetime.now().isocalendar()[1] - datetime(datetime.now().year, 1, 1).isocalendar()[1]
        return math.ceil(weeks_worked * self.vacation_accrual_multiplier())

    def week_started(self):
        end_of_year = date(date.today().year, 12, 31)
        if (end_of_year - self.start_date).days < 365:
            return self.start_date.isocalendar()[1]
        else:
            return 0

    def save(self, *args, **kwargs):
        self.vacation_hours = self.eligible_vacation_hours()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class SickAccrualOverride(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    sick_accrualed = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.employee.user.first_name} {self.employee.user.last_name}'

class EmployeeRate(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    effective_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('employee', 'effective_date')

    def __str__(self):
        return f'{self.employee.user.first_name} {self.employee.user.last_name} - $ {self.rate} from {self.effective_date}'

class PrevailingRate(models.Model):
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.CASCADE)
    effective_date = models.DateField(default=timezone.now)
    rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fringe_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_foremen = models.BooleanField(default=False)
    shift_differential = models.BooleanField(default=False) # extra pay for working a less desirable shift
    compressed_work_week = models.BooleanField(default=False) # four ten-hour days within a week rather than five eight-hour days

    def __str__(self):
        return f'{self.project.number} {self.project.name} - $ {self.rate}{" - Foreman Rate" if self.is_foremen else ""}'
