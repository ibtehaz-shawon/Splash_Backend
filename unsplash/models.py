from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class Photo(models.Model):
    photo_id = models.CharField(max_length=20,
                                unique=True,
                                primary_key=True,
                                validators=[alphanumeric])
    created_at = models.DateTimeField('date published', null=False)
    color = models.CharField(max_length=7, null=True, default="#ECFFC4")
    exif_make = models.CharField(max_length=50, null=True, default="null")
    exif_model = models.CharField(max_length=30, null=True, default="null")
    exif_exposure = models.CharField(max_length=30, null=True, default="null")
    exif_aparture = models.CharField(max_length=30, null=True, default="null")
    exif_focul = models.CharField(max_length=30, null=True, default="null")
    exif_iso = models.CharField(max_length=30, null=True, default="null")

    location_name = models.CharField(max_length=100, null=True, default="null")
    location_lat = models.FloatField(max_length=30, null=True, default="-1")
    location_long = models.FloatField(max_length=30, null=True, default="-1")

    url_raw = models.URLField(null=False)
    url_full = models.URLField(null=False)
    url_regular = models.URLField(null=False)
    url_download = models.URLField(null=False)
    url_share = models.URLField(null=False)

    user_display_name = models.CharField(max_length=100, null=False)
    user_profile_pic = models.URLField(null=True, default="null")
    photo_category = models.CharField(max_length=20, null=True, default="null")

