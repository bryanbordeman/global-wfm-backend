from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User

class DCN(models.Model):
    created_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    number = models.CharField(max_length=9, null= True) # 2023-001  YYYY-###
    rev = models.CharField(max_length=3, null=True, blank=True) ## rev A
    comments = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(250)])
    is_external = models.BooleanField(default=True) # if False DCN is internal
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.CASCADE)
    service = models.ForeignKey('project.Service', null=True, blank=True, on_delete=models.CASCADE)
    hse = models.ForeignKey('project.HSE', null=True, blank=True, on_delete=models.CASCADE)
    quote = models.ForeignKey('quote.Quote', null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.project:
            return f'{self.project} | {self.number}'
        elif self.service:
            return f'{self.service} | {self.number}'
        elif self.hse:
            return f'{self.hse} | {self.number}'
        else:
            return f'{self.quote} | {self.number}'

