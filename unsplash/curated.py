from django.contrib.sites import requests
from django.http import HttpResponse
import requests
import json

from unsplash.models import Photo
from unsplash.serializer import PhotoSerializer, CuratedSerializer
from unsplash_backend.settings import BEYBLADE_ID, UNSPLASH_BASE_URL


page_number = 1 #default

def get_curated_list(req):

    if req.method == 'GET':
        curated_feed = requests.get(UNSPLASH_BASE_URL + 'collections/curated/?client_id='
                                    + BEYBLADE_ID + '&page=' + str(1))
        try:
            feed_array = curated_feed.json()
            for counter in range(2, 3):
                curated_id = feed_array[counter]['id']
                curated_title = feed_array[counter]['title']
                curated_description = feed_array[counter]['description']
                curated_published = feed_array[counter]['published_at']
                curated_updated = feed_array[counter]['updated_at']
                curated_is_curated = bool(feed_array[counter]['curated'])
                curated_is_featured = bool(feed_array[counter]['featured'])
                curated_total_photos = feed_array[counter]['total_photos']

                curated_user_display = feed_array[counter]['user']['name']

                curated_user_profile_small = feed_array[counter]['user']['profile_image']['small']
                curated_user_profile_large = feed_array[counter]['user']['profile_image']['large']

                curated_cover_photo = single_photo_details(
                    feed_array[counter]['cover_photo'], counter, curated_user_display,
                    curated_user_profile_small, curated_user_profile_large)

                curated_collection_link_self = feed_array[counter]['links']['self']
                curated_collection_link_html = feed_array[counter]['links']['html']


                data = {
                    'curated_id': curated_id, 'curated_title': curated_title,
                    'curated_description': curated_description, 'curated_published': curated_published,
                    'curated_updated': curated_updated, 'curated_is_curated': curated_is_curated,
                    'curated_is_featured': curated_is_featured, 'curated_total_photos': curated_total_photos,
                    'curated_cover_photo': curated_cover_photo, 'curated_user_name': curated_user_display,
                    'curated_profile_image_small': curated_user_profile_small,
                    'curated_profile_image_large': curated_user_profile_large,
                    'curated_collection_url_self': curated_collection_link_self,
                    'curated_collection_url_html': curated_collection_link_html
                }

                serialized_data = CuratedSerializer(data=data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    print "$$$$$$ Current Counter is " + str(counter) + " and Success for " + \
                          str(curated_id)
                    return True
                else:
                    print "###### Current Counter is " + str(counter) + " and ERROR for ||" \
                          + str(curated_id) + "||"
                    print serialized_data.errors
                    return False
            return HttpResponse("Hello World")
        except ValueError as error:
            print "No JSON file " + str(error)
            return HttpResponse(str(error))





def single_photo_details(photo_data, counter, user_name, profile_pic_small, profile_pic_large):
    try:
        # ---------------------------------------------
        # Dumping the only necessary data in temporary variable
        # ---------------------------------------------
        photo_id = photo_data['id']
        created_at = photo_data['created_at']
        color = photo_data['color']
        photo_width = photo_data['width']
        photo_height = photo_data['height']


        url_thumb = photo_data['urls']['thumb']
        url_small = photo_data['urls']['small']
        url_regular = photo_data['urls']['regular']
        url_full = photo_data['urls']['full']
        # url_custom = photo_data['urls']['custom']
        url_custom = photo_data['urls']['regular']
        url_raw = photo_data['urls']['raw']
        url_download = photo_data['links']['download']
        url_share = photo_data['links']['html']

        # ---------------------------------------------
        # Inserting dump into a dictionary to insert---
        # ---------------------------------------------
        data = {'photo_id': photo_id, 'created_at': created_at, 'color': color,
                'photo_height': photo_height, 'photo_width': photo_width,
                'url_thumb': url_thumb, 'url_small': url_small, 'url_custom': url_custom,
                'url_raw': url_raw, 'url_full': url_full,
                'url_regular': url_regular, 'url_download': url_download, 'url_share': url_share,
                'user_display_name': user_name,
                'user_profile_pic': profile_pic_large,
                'user_profile_pic_small': profile_pic_small}
        # ---------------------------------------------
        # check serialize validation and insert--------
        # ---------------------------------------------
        serialized_data = PhotoSerializer(data=data)
        if serialized_data.is_valid():
            photo_unique_id = serialized_data.save()
            print str(photo_unique_id.photo_id) + " ||success for|| "+ str(counter)
            return photo_unique_id.photo_id

        else:
            print " ||ERRor for|| " + str(counter)
            return get_single_photo(photo_id)
    except ValueError as error:
        print " ||ERRor for|| " + str(counter) + " error is "+ str(error)
        return get_single_photo(photo_id)



def get_single_photo(photo_id):
    single_photo = Photo.objects.get(photo_id = str(photo_id))
    return single_photo.photo_id
