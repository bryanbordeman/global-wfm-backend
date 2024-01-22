from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class WorkOrderRev(models.Model):
    rev = models.CharField(max_length=3, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(1000)])
    issue_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Rev {self.rev} {self.issue_date}'
    
class PartCategory(models.Model):
    description = models.CharField(max_length=400)

    def __str__(self):
        return f'{self.description}'
    
class PartAttribute(models.Model):
    description = models.CharField(max_length=400)
    
    def __str__(self):
        return f'{self.description}'

class Part(models.Model):
    manufacturer = models.ForeignKey('contact.Company', null=True, blank=True, on_delete=models.PROTECT)
    manufacturer_part_number = models.CharField(max_length=400, blank=True)
    categories = models.ManyToManyField(PartCategory,  blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=8000, blank=True,
                                validators=[MaxLengthValidator(8000)])
    drawings = models.ManyToManyField('uploader.drawing', blank=True) # drawings are only pdfs.
    attachments = models.ManyToManyField('uploader.DropBox', blank=True) # attachments are only images.

class WorkOrderPart(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    attributes = models.ManyToManyField(PartAttribute,  blank=True)

class WorkOrder(models.Model):
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    service = models.ForeignKey('project.Service', null=True, blank=True, on_delete=models.PROTECT)
    hse = models.ForeignKey('project.HSE', null=True, blank=True, on_delete=models.PROTECT)
    rev = models.ManyToManyField(WorkOrderRev, blank=True)
    due = models.DateField(null=True)
    issue_date = models.DateField(null=True)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
    checked_by = models.ForeignKey(User, related_name='checked_by', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assigned', on_delete=models.CASCADE)
    parts = models.ManyToManyField(WorkOrderPart, blank=True)
    is_complete = models.BooleanField(default=False) # when ready to ship
    completed = models.DateTimeField(null=True, blank=True, auto_now_add=True, editable=True) # when shipped
    updated = models.DateTimeField(null=True, blank=True, auto_now_add=True, editable=True)

    def __str__(self):
        project = ''

        if self.project != None:
            project = self.project.number
        elif self.service != None:
            project = self.service.number
        elif self.hse != None:
            project = self.hse.number
        
        return f'{project}'

class BillOfMaterials(models.Model):
    materials = models.ManyToManyField(WorkOrder, blank=True)