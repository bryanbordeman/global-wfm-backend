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
    rev = models.CharField(max_length=3, null=True, blank=True)
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.PROTECT)
    service = models.ForeignKey('project.Service', null=True, blank=True, on_delete=models.PROTECT)
    hse = models.ForeignKey('project.HSE', null=True, blank=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=150, editable=False)
    title_suffix = models.CharField(max_length=150, blank=True)
    document = models.FileField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.service:
            number = self.service.number
        elif self.hse:
            number = self.hse.number
        else:
            number = self.project.number
        self.title = f'{number} {self.drawing_type.description}{f" {self.title_suffix}" if self.title_suffix else ""}{f" Rev {self.rev}" if self.rev else ""}'
        super(Drawing, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Drawings'

    def __str__(self):
        return f'{self.title}'
    

class VideoCategory(models.Model):
    description = models.CharField(max_length=400)
    
    class Meta:
        verbose_name_plural = 'Video Categories'

    def __str__(self):
        return f'{self.description}'

class VideoThumbnail(models.Model):
    title = models.CharField(max_length=150)
    document = models.FileField(max_length=150, upload_to='videos/thumbnails')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Video Thumbnails'

    def __str__(self):
        return f'{self.title}'

class Video(models.Model):
    title = models.CharField(max_length=150)
    thumbnail = models.ForeignKey(VideoThumbnail, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True)
    document = models.FileField(max_length=150, upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Videos'

    def __str__(self):
        return f'{self.title}'