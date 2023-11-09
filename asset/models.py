from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class AssetType(models.Model):
    description = models.CharField(max_length=200)
    code = models.CharField(max_length=3)

class AssetLog(models.Model):
    description = models.CharField(max_length=200)
    date = models.DateField()

class BaseAsset(models.Model):
    is_active = models.BooleanField(null= False, default=True)
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True)
    logs = models.ManyToManyField(AssetLog, blank=True)
    qr_code = models.ForeignKey('uploader.dropbox', on_delete=models.SET_NULL, blank=True, null=True)
    serial_code = models.CharField(max_length=20)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    created = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True
    
class Tool(BaseAsset):
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.serial_code}'
    
class Material(BaseAsset):
    quantity = models.IntegerField(null=True, blank=True,)
    def __str__(self):
        return f'{self.serial_code}'

# --- Door Objects --- #

class DoorReport(models.Model):
    STATUS_CHOICES = [
    ("Complete", "Complete"),
    ("Incomplete", "Incomplete"),
    ("Pending for spares", "Pending for spares"),
    ("Under Observation", "Under Observation"),
    ("Working solution provided", "Working solution provided"),
    ]
    SERVICE_TYPE_CHOICES = [
    ("Emergency ", "Emergency "),
    ("Warranty", "Warranty"),
    ("Scheduled Maintenance", "Scheduled Maintenance"),
    ]
    status = models.CharField( max_length=200, choices=STATUS_CHOICES, default="Complete")
    service_type = models.CharField( max_length=200, choices=SERVICE_TYPE_CHOICES, default="Complete")
    service_rendered = models.TextField(max_length=3000, blank=True,
                                validators=[MaxLengthValidator(3000)])
    problem_reported = models.TextField(max_length=3000, blank=True, null=True,
                                validators=[MaxLengthValidator(3000)])
    date = models.DateField()
    technician = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return f'Service {self.id} on {self.date}'
    
class DoorRev(models.Model):
    rev = models.CharField(max_length=3, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(1000)])
    issue_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Rev {self.rev} {self.issue_date}'

class BaseDoorAttribute(models.Model):
    description = models.CharField(max_length=400)
    
    class Meta:
        abstract = True

class DoorLockset(BaseDoorAttribute):
    def __str__(self):
        return f'{self.description}'

class DoorType(BaseDoorAttribute):
    def __str__(self):
        return f'{self.description}'

class DoorSillType(BaseDoorAttribute):
    def __str__(self):
        return f'{self.description}'

class DoorFrameType(BaseDoorAttribute):
    def __str__(self):
        return f'{self.description}'

class DoorCoreType(BaseDoorAttribute):
    def __str__(self):
        return f'{self.description}'

class DoorHingeType(BaseDoorAttribute):
    def __str__(self):
        return f'{self.description}'

class DoorOptions(BaseDoorAttribute):
    def __str__(self):
        return f'{self.description}'

class DoorPackaging(BaseDoorAttribute):
    def __str__(self):
        return f'{self.description}'

class Door(models.Model):
    HAND_CHOICES = [
    ("RH", "Right Hand"),
    ("LH", "Left Hand"),
    ("RHA", "Right Hand Active"),
    ("LHA", "Left Hand Active"),
    ("BI", "Bi-Parting")
    ]

    SWING_CHOICES = [
    ("in", "In Swing"),
    ("out", "Out Swing"),
    ]

    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    service = models.ForeignKey('project.Service', null=True, blank=True, on_delete=models.PROTECT)
    rev = models.ManyToManyField(DoorRev, blank=True)
    due = models.DateField(null=True)
    issue_date = models.DateField(null=True)
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    checked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    hand = models.CharField( max_length=200, choices=HAND_CHOICES, default="RH")
    swing = models.CharField( max_length=200, choices=SWING_CHOICES, default="in")
    door_type = models.ForeignKey(DoorType, on_delete=models.SET_NULL, null=True)
    is_double_door = models.BooleanField(default=False) # if door_type = double
    is_sliding = models.BooleanField(default=False) 
    is_biparting = models.BooleanField(default=False) 
    inactive_width = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=3)
    height = models.DecimalField(max_digits=10, decimal_places=3)
    veneer = models.CharField(max_length=200)
    lockset = models.ForeignKey(DoorLockset, on_delete=models.SET_NULL, null=True)
    door_switch = models.BooleanField(default=True)
    sill_type = models.ForeignKey(DoorSillType, on_delete=models.SET_NULL, null=True)
    frame_type = models.ForeignKey(DoorFrameType, on_delete=models.SET_NULL, null=True)
    core_type = models.ForeignKey(DoorCoreType, on_delete=models.SET_NULL, null=True)
    hinge_type = models.ForeignKey(DoorHingeType, on_delete=models.SET_NULL, null=True)
    options = models.ManyToManyField(DoorOptions, blank=True)
    packaging = models.ForeignKey(DoorPackaging, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(1000)])
    is_complete = models.BooleanField(default=False) # when door ships
    completed = models.DateTimeField(null=True, blank=True, auto_now_add=True, editable=True) # when door ships
    updated = models.DateTimeField(null=True, blank=True, auto_now_add=True, editable=True)
    drawings = models.ManyToManyField('uploader.drawing', blank=True)
    log = models.ManyToManyField(DoorReport, blank=True,)
    qr_code = models.ForeignKey('uploader.dropbox', on_delete=models.CASCADE, blank=True, null=True)
    count = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            # New door, assign count number
            door_count = Door.objects.filter(project=self.project).count()
            self.count = door_count + 1
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.project.number} {self.hand} {self.swing}'

