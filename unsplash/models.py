from __future__ import unicode_literals

import uuid
from mx.DateTime import Timezone

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


# use default = none
class Photo(models.Model):
    photo_id = models.CharField(max_length=20,
                                unique=True,
                                primary_key=True)

    created_at = models.DateTimeField('date published', null=False)
    updated_at = models.DateTimeField('date updated', null=True)

    color = models.CharField(max_length=7, null=True, default="#ECFFC4")

    exif_make = models.CharField(max_length=50, null=True, default="none", blank=True)
    exif_model = models.CharField(max_length=30, null=True, default="none", blank=True)
    exif_exposure = models.CharField(max_length=30, null=True, default="none", blank=True)
    exif_aperture = models.CharField(max_length=30, null=True, default="none", blank=True)
    exif_focal = models.CharField(max_length=30, null=True, default="none", blank=True)
    exif_iso = models.CharField(max_length=30, null=True, default="none", blank=True)

    location_name = models.CharField(max_length=100, null=True, default="none")
    location_lat = models.FloatField(max_length=30, null=True, default="-1")
    location_long = models.FloatField(max_length=30, null=True, default="-1")

    url_thumb = models.URLField(null=False, default="none")
    url_small = models.URLField(null=False, default="none")
    url_regular = models.URLField(null=False)
    url_full = models.URLField(null=False)
    url_custom = models.URLField(null=False, default="none")
    url_raw = models.URLField(null=False)
    url_download = models.URLField(null=False)
    url_share = models.URLField(null=False)

    user_display_name = models.CharField(max_length=100, null=False)
    user_profile_pic = models.URLField(null=True, default="none")
    user_profile_pic_small = models.URLField(null=True, default="none")
    photo_category = models.CharField(max_length=20, null=True, default="none")

    photo_height = models.CharField(max_length=5, null=False, default="none")
    photo_width = models.CharField(max_length=5, null=False, default="none")

    curated_id = models.ForeignKey('CollectionList', null=True)


#Device Data table

class DeviceData(models.Model):
    device_id = models.CharField(max_length=100, unique=True, null=False)
    device_height = models.CharField(max_length=100, null=False)
    device_width = models.CharField(max_length=100, null=False)
    unique_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)



#Curated List & Featured List
class CollectionList(models.Model):
    curated_id = models.CharField(max_length=100, primary_key=True, unique=True, null=False)
    curated_title = models.CharField(max_length= 200, blank=False, null=False)
    curated_description = models.CharField(max_length=500, blank=False, null=False)

    curated_published = models.DateTimeField('date published', null=False)
    curated_updated = models.DateTimeField('date updated', null=False)

    curated_is_curated = models.BooleanField(max_length=30, null=False, default=False)
    curated_is_featured = models.BooleanField(max_length=30, null=False, default=False)
    curated_total_photos = models.CharField(max_length=4, null=False, default=0)

    curated_cover_photo = models.ForeignKey('Photo', null=False)

    curated_user_name = models.CharField(max_length=30, null=False, blank=False)

    curated_profile_image_small = models.URLField(null=True, default="none")
    curated_profile_image_large = models.URLField(null=True, default="none")

    curated_collection_url_self = models.URLField(null=False, blank=False)
    curated_collection_url_html = models.URLField(null=False, blank=False)



