from django.contrib import admin
from .models import DoorReport
from .models import DoorRev
from .models import DoorLockset
from .models import DoorType
from .models import DoorSillType
from .models import DoorFrameType
from .models import DoorCoreType
from .models import DoorHingeType
from .models import DoorOptions
from .models import DoorPackaging
from .models import Door

admin.site.register(DoorReport)
admin.site.register(DoorRev)
admin.site.register(DoorLockset)
admin.site.register(DoorType)
admin.site.register(DoorSillType)
admin.site.register(DoorFrameType)
admin.site.register(DoorCoreType)
admin.site.register(DoorHingeType)
admin.site.register(DoorOptions)
admin.site.register(DoorPackaging)
admin.site.register(Door)

