from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from unsplash.models import Photo
from django.core import serializers
import requests
import json

from unsplash.serializer import PhotoSerializer
from unsplash_backend.settings import UNSPLASH_ID, UNSPLASH_BASE_URL


def index(req):
    r = requests.get(UNSPLASH_BASE_URL+'photos/Xeizdya0cbs?client_id='+UNSPLASH_ID)
    photoData = r.json()
    # ---------------------------------------------
    # Dumping the only necessary data in temporary variable
    # ---------------------------------------------
    photoID = photoData['id']
    createdAt = photoData['created_at']
    color = photoData['color']

    exif_make = photoData['exif']['make']
    if len(exif_make) > 50:
        exif_make = exif_make[:50]
    exif_model = photoData['exif']['model']
    exif_exposure = photoData['exif']['exposure_time']
    exif_aparture = photoData['exif']['aperture']
    exif_focal = photoData['exif']['focal_length']
    exif_iso = photoData['exif']['iso']

    if 'location' in photoData:
        location_name = photoData['location']['title']
        if len(location_name) > 100:
            location_name = location_name[:100]
        location_lat = photoData['location']['position']['latitude']
        location_long = photoData['location']['position']['longitude']
    else:
        location_name = "null"
        location_lat = -1
        location_long = -1

    url_full = photoData['urls']['full']
    url_regular = photoData['urls']['regular']
    url_download = photoData['links']['download']
    url_share = photoData['links']['html']

    user_display_name = photoData['user']['name']
    if len(user_display_name) > 100:
        user_display_name = user_display_name[:100]
    user_profile_pic = photoData['user']['profile_image']['medium']
    # ---------------------------------------------
    # Inserting dump into a dictionary to insert
    # ---------------------------------------------
    data = {}
    data['photo_id'] = photoID
    data['created_at'] = createdAt
    data['color'] = color
    data['exif_make'] = exif_make
    data['exif_model'] = exif_model
    data['exif_exposure'] = exif_exposure
    data['exif_aparture'] = exif_aparture
    data['exif_focul'] = exif_focal
    data['exif_iso'] = exif_iso
    data['location_name'] = location_name
    data['location_lat'] = location_lat
    data['location_long'] = location_long
    data['url_raw'] = url_full
    data['url_full'] = url_full
    data['url_regular'] = url_regular
    data['url_download'] = url_download
    data['url_share'] = url_share
    data['user_display_name'] = user_display_name
    data['user_profile_pic'] = user_profile_pic
    # ---------------------------------------------
    # check serialize validation and insert--------
    # ---------------------------------------------
    serialized_data = PhotoSerializer(data=data)
    if serialized_data.is_valid():
        serialized_data.save()
        return HttpResponse("Successfully Saved!")
    else:
        print serialized_data.errors
        return HttpResponse("Oh! An Error occured!")



def getFeed(req):
    latest_photos = Photo.objects.order_by('-created_at')[:10]
    output = serializers.serialize("json", latest_photos)
    return HttpResponse(output, content_type='application/json')
