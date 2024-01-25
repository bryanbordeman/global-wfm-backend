from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_salary = models.BooleanField(default=False)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    documents = models.ManyToManyField('uploader.DropBox', blank=True) # attachments are only images for now.

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class EmployeeRate(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    effective_date = models.DateField()

    class Meta:
        unique_together = ('employee', 'effective_date')

    def __str__(self):
        return f'{self.employee.user.first_name} {self.employee.user.last_name} - $ {self.rate} from {self.effective_date}'
    
class PrevailingRate(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.CASCADE)
    service = models.ForeignKey('project.Service', null=True, blank=True, on_delete=models.CASCADE)
    hse = models.ForeignKey('project.HSE', null=True, blank=True, on_delete=models.CASCADE)
    quote = models.ForeignKey('quote.Quote', null=True, blank=True, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.project.number} {self.project.name} - $ {self.rate}'