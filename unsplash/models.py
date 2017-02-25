from __future__ import unicode_literals

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
