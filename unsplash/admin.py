from django.contrib import admin
from models import Photo, DeviceData, CuratedList

# Register your models here.

admin.site.register(Photo)
admin.site.register(DeviceData)
admin.site.register(CuratedList)