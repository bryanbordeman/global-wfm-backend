from django.db import models
from django.core.validators import MaxLengthValidator
from imagekit.models.fields import ProcessedImageField

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
    qr_code = ProcessedImageField(default='qrcode.png', format='PNG', upload_to='None', options={'quality': 20})
    serial_code = models.CharField(max_length=20)
    notes = models.TextField(max_length=250, blank=True,
                                validators=[MaxLengthValidator(250)])
    created = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True

class Door(BaseAsset):
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    customer = models.ForeignKey('contact.Company', on_delete=models.PROTECT)
    address = models.ForeignKey('contact.Address', null=True, blank=True, on_delete=models.PROTECT)
    def __str__(self):
        return f'{self.serial_code}'
    
class Tool(BaseAsset):
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.serial_code}'
    
class Material(BaseAsset):
    quantity = models.IntegerField(null=True, blank=True,)
    def __str__(self):
        return f'{self.serial_code}'