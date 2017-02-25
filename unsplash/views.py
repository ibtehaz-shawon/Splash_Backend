from django.contrib.sites import requests
from django.http import HttpResponse
from unsplash.models import Photo
import requests
import json
import unicodedata

from unsplash.serializer import PhotoSerializer
from unsplash_backend.settings import BEYBLADE_ID, UNSPLASH_BASE_URL, POKEMON_ID

"""
This function originally does not take any request from production, only work to insert more item in the
 database
:req
:return SUCCESS message for successful database input
"""

CUSTOM_HEIGHT = 3840
CUSTOM_WIDTH = 2000
MAX_LOOP = 6


def index(req):
    total_success = 0
    total_failure = 0
    for page_number in range(1, MAX_LOOP, 1):
        random_feed = requests.get(UNSPLASH_BASE_URL + 'photos/?client_id=' + BEYBLADE_ID + '&page=' + str(page_number))
        if random_feed.text == 'Rate Limit Exceeded':
            print "$$$$ ---- LIMIT EXCEEDED ---- $$$$ in " + str(page_number)
            html_message = "$$$$ ---- LIMIT EXCEEDED ---- $$$$ in " + str(page_number) \
                           + " Total Success: " + str(total_success) + " Total Failure: " + str(total_failure)
            return HttpResponse(html_message)
            break
        else:
            try:
                feed_array = random_feed.json()
            except ValueError as error:
                print "No JSON file "+str(error)
                return HttpResponse(str(error))

            for counter in range(0, 10):
                current_photo_id = feed_array[counter]['id']
                photo_details_url = requests.get(
                    UNSPLASH_BASE_URL + 'photos/' + current_photo_id + '?client_id=' + BEYBLADE_ID +
                    '&w=' + str(CUSTOM_WIDTH) + '&h=' + str(CUSTOM_HEIGHT))

                if photo_details_url.text == 'Rate Limit Exceeded':
                    print "$$$$ ---- LIMIT EXCEEDED ---- $$$$ in " + str(page_number)
                    html_message = "$$$$ ---- LIMIT EXCEEDED ---- $$$$ in " + str(page_number) \
                                   + " Total Success: " + str(total_success) + " Total Failure: " + str(total_failure)
                    return HttpResponse(html_message)
                    break
                else:
                    flag = single_photo_details(photo_details_url.json(), page_number)

                if flag:
                    total_success += 1
                else:
                    total_failure += 1

    print "Total Success: " + str(total_success) + " Total Failure: " + str(total_failure)
    return HttpResponse("Total Success: " + str(total_success) + " Total Failure: " + str(total_failure))


"""
functions takes a GET arguments and returned the latest_photos sorted by created_at at ascending order.
pagination implemented to send 10 data at once.
:requests GET
:page url parameter, default 1;
:return
feed data ALL at once.
feed data 10 at a time. [updated]
"""


def get_feed(req):
    if req.method == 'GET':
        latest_photos = Photo.objects.order_by('-created_at')
        response_data = {}
        photo_data = []
        counter = 0
        try:
            current_page = int(req.GET.get('page', "1"))
            print req.GET.get('page', "1")
        except ValueError as error:
            current_page = 1
            print str(error)

        upper_limit = int(current_page * 10)
        lower_limit = int(upper_limit) - 10 + 1
        total = 0

        for entry in latest_photos:
            counter += 1
            if lower_limit <= counter <= upper_limit:
                new_photo_data = {'photo_id': str(entry.photo_id),
                                  'created_at': str(entry.created_at),
                                  'color': str(entry.color),
                                  'height': str(entry.photo_height),
                                  'width': str(entry.photo_width),

                                  'user_camera_make': str(entry.exif_make),
                                  'user_camera_model': str(entry.exif_model),
                                  'user_camera_exposure': str(entry.exif_exposure),
                                  'user_camera_apature': str(entry.exif_aperture),
                                  'user_camera_focal': str(entry.exif_focal),
                                  'user_camera_iso': str(entry.exif_iso),

                                  'photo_location_name': unicodedata.normalize('NFKD', entry.location_name).encode('ascii',
                                                                                                                   'ignore'),
                                  'photo_location_lat': str(entry.location_lat),
                                  'photo_location_long': str(entry.location_long),

                                  'url_thumb': str(entry.url_thumb),
                                  'url_small': str(entry.url_small),
                                  'url_raw': str(entry.url_raw),
                                  'url_full': str(entry.url_full),
                                  'url_regular': str(entry.url_regular),
                                  'url_custom': str(entry.url_custom),
                                  'url_download': str(entry.url_download),
                                  'url_share': str(entry.url_share),

                                  'user_display_name': entry.user_display_name,
                                  'user_profile_pic': str(entry.user_profile_pic),
                                  'user_profile_pic_small': str(entry.user_profile_pic_small),
                                  'photo_category': str(entry.photo_category)}
                photo_data.append(new_photo_data)
                total += 1

        response_data['total'] = total
        response_data['photo'] = photo_data
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        error_response = {'error': 'error occurred', 'message': 'unknown method'}
        return HttpResponse(json.dump(error_response), content_type='application/json')


"""
functions take one parameter (photo_data) in JSON format and parses, create a dictionary and send it to
Model (Photo) via Serializer.
"""


def single_photo_details(photo_data, counter):
    try:
        # ---------------------------------------------
        # Dumping the only necessary data in temporary variable
        # ---------------------------------------------
        photo_id = photo_data['id']
        created_at = photo_data['created_at']
        color = photo_data['color']
        photo_width = photo_data['width']
        photo_height = photo_data['height']

        exif_make = photo_data['exif']['make']
        if len(exif_make) > 50:
            exif_make = exif_make[:50]
        exif_model = photo_data['exif']['model']
        exif_exposure = photo_data['exif']['exposure_time']
        exif_aperture = photo_data['exif']['aperture']
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

        url_thumb = photo_data['urls']['thumb']
        url_small = photo_data['urls']['small']
        url_regular = photo_data['urls']['regular']
        url_full = photo_data['urls']['full']
        url_custom = photo_data['urls']['custom']
        url_raw = photo_data['urls']['raw']
        url_download = photo_data['links']['download']
        url_share = photo_data['links']['html']

        user_display_name = photo_data['user']['name']
        if len(user_display_name) > 100:
            user_display_name = user_display_name[:100]

        user_profile_pic_small = photo_data['user']['profile_image']['small']
        user_profile_pic = photo_data['user']['profile_image']['large']
        # ---------------------------------------------
        # Inserting dump into a dictionary to insert---
        # ---------------------------------------------
        data = {'photo_id': photo_id, 'created_at': created_at, 'color': color,
                'photo_height': photo_height, 'photo_width': photo_width,
                'exif_make': exif_make,
                'exif_model': exif_model, 'exif_exposure': exif_exposure, 'exif_aperture': exif_aperture,
                'exif_focal': exif_focal, 'exif_iso': exif_iso, 'location_name': location_name,
                'location_lat': location_lat, 'location_long': location_long,
                'url_thumb': url_thumb, 'url_small': url_small, 'url_custom': url_custom,
                'url_raw': url_raw, 'url_full': url_full,
                'url_regular': url_regular, 'url_download': url_download, 'url_share': url_share,
                'user_display_name': user_display_name,
                'user_profile_pic': user_profile_pic, 'user_profile_pic_small': user_profile_pic_small}
        # ---------------------------------------------
        # check serialize validation and insert--------
        # ---------------------------------------------
        serialized_data = PhotoSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            print "$$$$$$ Current Counter is " + str(counter) + " and Success for " + photo_id
            return True
        else:
            print "###### Current Counter is " + str(counter) + " and ERROR for ||" + photo_id + "||"
            print serialized_data.errors
            return False
    except ValueError as error:
        print "Error occurred "+str(error)
        return False
