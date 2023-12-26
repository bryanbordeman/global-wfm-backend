from django.contrib import admin
from .models import DropBox
from .models import DrawingType
from .models import Drawing
from .models import Video
from .models import VideoCategory
from .models import VideoThumbnail

admin.site.register(DropBox)
admin.site.register(DrawingType)
admin.site.register(Drawing)
admin.site.register(Video)
admin.site.register(VideoCategory)
admin.site.register(VideoThumbnail)