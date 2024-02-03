from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.utils import timezone

class Benefit(models.Model):
    description = models.CharField(max_length=200, null= True)

    def __str__(self):
        return f'{self.description}'

class EmployeeBenefit(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    employer_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.benefit.description} - {self.employee.user.first_name} {self.employee.user.last_name}{" - Employer Paid" if self.employer_paid else ""}'

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    is_salary = models.BooleanField(default=False)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    documents = models.ManyToManyField('uploader.DropBox', blank=True) # attachments are only images for now.
    vacation_hours = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    holiday_hours = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    sick_hours = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    benefits = models.ManyToManyField(Benefit, through='EmployeeBenefit', blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

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
    segment = models.ManyToManyField('worksegment.WorkSegment', blank=True)
    effective_date = models.DateField(default=timezone.now)
    rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fringe_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_foremen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.project.number} {self.project.name} - $ {self.rate}{" - Foreman Rate" if self.is_foremen else ""}'
    

 # life_insurance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # long_term_disability = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # dental = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # vision = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # health = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # health_employee_paid = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
