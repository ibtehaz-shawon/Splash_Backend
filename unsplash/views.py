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
    for page_number in range(0, 5):
        random_feed = requests.get(UNSPLASH_BASE_URL + 'photos/?client_id=' + UNSPLASH_ID+'&page='+str(page_number))
        if random_feed.text == '403 Forbidden (Rate Limit Exceeded)':
            print "$$$$ ---- LIMIT EXCEEDED ---- $$$$"
        else:
            feed_array = random_feed.json()
            for x in range(0, 9):
                current_photo_id = feed_array[x]['id']
                print 'Parsing '+current_photo_id
                photo_details_url = requests.get(UNSPLASH_BASE_URL + 'photos/' + current_photo_id + '?client_id=' + UNSPLASH_ID)
                single_photo_details(photo_details_url.json())
    return HttpResponse("Hello World")


def getFeed(req):
    latest_photos = Photo.objects.order_by('-created_at')
    output = serializers.serialize("json", latest_photos)
    return HttpResponse(output, content_type='application/json')


"""
functions take one parameter (photo_data) in JSON format and parses, create a dictionary and send it to
Model (Photo) via Serializer.
"""
def single_photo_details(photo_data):
    # ---------------------------------------------
    # Dumping the only necessary data in temporary variable
    # ---------------------------------------------
    photo_id = photo_data['id']
    created_at = photo_data['created_at']
    color = photo_data['color']

    exif_make = photo_data['exif']['make']
    if len(exif_make) > 50:
        exif_make = exif_make[:50]
    exif_model = photo_data['exif']['model']
    exif_exposure = photo_data['exif']['exposure_time']
    exif_aparture = photo_data['exif']['aperture']
    exif_focal = photo_data['exif']['focal_length']
    exif_iso = photo_data['exif']['iso']

    if 'location' in photo_data:
        location_name = photo_data['location']['title']
        if len(location_name) > 100:
            location_name = location_name[:100]
        location_lat = photo_data['location']['position']['latitude']
        location_long = photo_data['location']['position']['longitude']
    else:
        location_name = "null"
        location_lat = -1
        location_long = -1

    url_full = photo_data['urls']['full']
    url_regular = photo_data['urls']['regular']
    url_download = photo_data['links']['download']
    url_share = photo_data['links']['html']

    user_display_name = photo_data['user']['name']
    if len(user_display_name) > 100:
        user_display_name = user_display_name[:100]
    user_profile_pic = photo_data['user']['profile_image']['medium']
    # ---------------------------------------------
    # Inserting dump into a dictionary to insert
    # ---------------------------------------------
    data = {'photo_id': photo_id, 'created_at': created_at, 'color': color, 'exif_make': exif_make,
            'exif_model': exif_model, 'exif_exposure': exif_exposure, 'exif_aparture': exif_aparture,
            'exif_focul': exif_focal, 'exif_iso': exif_iso, 'location_name': location_name,
            'location_lat': location_lat, 'location_long': location_long, 'url_raw': url_full, 'url_full': url_full,
            'url_regular': url_regular, 'url_download': url_download, 'url_share': url_share,
            'user_display_name': user_display_name, 'user_profile_pic': user_profile_pic}
    # ---------------------------------------------
    # check serialize validation and insert--------
    # ---------------------------------------------
    serialized_data = PhotoSerializer(data=data)
    if serialized_data.is_valid():
        serialized_data.save()
        print "Success"
    else:
        print serialized_data.errors