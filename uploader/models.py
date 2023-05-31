from django.db import models

class DropBox(models.Model):
    title = models.CharField(max_length=150)
    document = models.FileField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Drop Boxes'

    def __str__(self):
        return f'{self.title}'

class DrawingType(models.Model):
    ''' Submittal, Fabrication, Sketch....'''
    description = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.description}'

class Drawing(models.Model):
    is_active = models.BooleanField(null= False, default=True)
    drawing_type = models.ForeignKey(DrawingType, on_delete=models.SET_NULL, null=True)
    rev = models.IntegerField(null=True, blank=True, default=0)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=150, editable=False)
    document = models.FileField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.title = f'{self.project.number} {self.drawing_type.description} Rev {self.rev}'
        super(Drawing, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Drawings'

    def __str__(self):
        return f'{self.title}'