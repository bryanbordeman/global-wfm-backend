from django.db import models
from django.core.validators import MaxLengthValidator

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(max_length=1000, blank=True,
                                validators=[MaxLengthValidator(1000)])
    #set to current time
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title