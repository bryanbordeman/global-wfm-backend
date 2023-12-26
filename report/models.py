from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from isoweek import Week

class BaseReport(models.Model):
    number = models.CharField(max_length=30, blank=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    quote = models.ForeignKey('quote.Quote', null=True, blank=True, on_delete=models.PROTECT)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    service = models.ForeignKey('project.Service', null=True, blank=True, on_delete=models.PROTECT)
    hse = models.ForeignKey('project.HSE', null=True, blank=True, on_delete=models.PROTECT)
    comments = models.TextField(max_length=2500, blank=True,
                                validators=[MaxLengthValidator(5000)])
    date = models.DateField(null=True)
    isoweek = models.CharField(max_length=8, blank=True, editable=False)
    attachments = models.ManyToManyField('uploader.DropBox', blank=True) # attachments are only images for now.
    is_active = models.BooleanField(null= False, default=True) # if False report is archived

    def save(self, *args, **kwargs):
        'convert date to isoweek'
        self.isoweek = Week.withdate(self.date)

        'report number = project number plus report id. example 12345.1'
        project = ''
        if self.project != None:
            project = self.project.number
        elif self.service != None:
            project = self.service.number
        elif self.hse != None:
            project = self.hse.number
        elif self.quote != None:
            project = self.quote.number
        
        self.number = f'{project}.{self.id}'

        super(BaseReport, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class ProjectReport(BaseReport):

    def __str__(self):
        return f'Report Number: {self.number} | Date: {self.date} | Week: {self.isoweek} | User: {self.user.first_name} {self.user.last_name}'

class DoorServiceReport(BaseReport):
    STATUS_CHOICES = [('Complete','Complete'),
                ('Incomplete','Incomplete'),
                ('Pending','Pending'),
                ('Under Observation','Under Observation'),
                ('Working solution provided','Working solution provided')]
    SERVICE_TYPE_CHOICES = [
                ("Emergency ", "Emergency "),
                ("Warranty", "Warranty"),
                ("Scheduled Maintenance", "Scheduled Maintenance"),
                ]
    technician = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    door = models.ForeignKey('asset.Door', null=True, blank=True, on_delete=models.PROTECT)
    
    status = models.CharField(max_length=200, null=True, choices=STATUS_CHOICES)
    service_type = models.CharField( max_length=200, choices=SERVICE_TYPE_CHOICES, default="Scheduled Maintenance")
    problem_reported = models.TextField(max_length=5000, blank=True,
                                validators=[MaxLengthValidator(5000)])
    service_rendered = models.TextField(max_length=5000, blank=True,
                                validators=[MaxLengthValidator(5000)])

    def __str__(self):
        return f'Report Number: {self.number} | Date: {self.date} | Week: {self.isoweek} | User: {self.user.first_name} {self.user.last_name}'

class IncidentReport(BaseReport):
    CHOICES = (('Shop','Shop'),
                ('Field','Field'),
                ('Office','Office'),)
    witnesses =  models.TextField(max_length=300, blank=True,
                                validators=[MaxLengthValidator(300)])
    participants = models.TextField(max_length=300, blank=True,
                                validators=[MaxLengthValidator(300)])
    location = models.TextField(max_length=300, blank=True,
                                validators=[MaxLengthValidator(300)])
    category = models.CharField(max_length=200, null=True, choices=CHOICES)

    def __str__(self):
        return f'Report Number: {self.number} | Date: {self.date} | Week: {self.isoweek} | User: {self.user.first_name} {self.user.last_name}'
