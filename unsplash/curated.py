import codecs
import unicodedata
from django.contrib.sites import requests
from django.db import IntegrityError
from django.http import HttpResponse
import requests
import json

from unsplash.models import Photo, CollectionList
from unsplash.serializer import PhotoSerializer, CuratedSerializer
from unsplash_backend.settings import BEYBLADE_ID, UNSPLASH_BASE_URL


PAGE_NUMBER = 2 #default


"""
-----------------------------------------------------------
-----------------------------------------------------------
contains/handle the curated list creation from unsplash.
example url: BASE_URL + /unsplash/collection?method=1 or 2
method: 1-> curated collections
method: 2-> featured collections
@:parameter -> url will send the page number, if no page number found, default is 1
-----------------------------------------------------------
-----------------------------------------------------------
"""

def get_curated_list(req):
    if req.method == 'GET':
        current_method = int(req.GET.get('method', "1"))

        if current_method == 1:
            curated_feed = requests.get(UNSPLASH_BASE_URL + 'collections/curated/?client_id='
                                    + BEYBLADE_ID + '&page=' + str(PAGE_NUMBER))
        else:
            curated_feed = requests.get(UNSPLASH_BASE_URL + 'collections/featured/?client_id='
                                        + BEYBLADE_ID + '&page=' + str(PAGE_NUMBER))
        success = 0
        failure = 0
        print "Running method -> "+str(current_method)
        try:
            feed_array = curated_feed.json()
            for counter in range(0, 10):
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
                    curated_user_profile_small, curated_user_profile_large, False)

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
                    print "$$$$$$ current method: "+str(current_method)  +" Current Counter is " + str(counter) + " and Success for " + str(curated_id)
                    success += 1
                else:
                    print "@@@@@@ current method: "+str(current_method)  +" Current Counter is " + str(counter) + " and ERROR for ||" + str(curated_id) + "||"
                    failure += 1
                    print serialized_data.errors
        except ValueError as error:
            print "No JSON file " + str(error)

        print "Total Success: "+str(success) + " Total Failure: "+str(failure)
        return HttpResponse("Hello World "+ "Total Success: "+str(success) + " Total Failure: "+str(failure))



"""
-----------------------------------------------------------
-----------------------------------------------------------
functions take one parameter (photo_data) in JSON format and parses, create a dictionary and send it to
Model (Photo) via Serializer.
@:photo_data photo_data -> photo data in JSON format to parse
@:counter counter -> current counter in the loop
@:user_name -> to insert it with the cover photo id.
@:profile_pic_small -> profile pic of the curated collections users
@:profile_pic_large -> large profile pic of the curated collections users.
@:return photo_id of the newly inserted/already existed photo id.
-----------------------------------------------------------
-----------------------------------------------------------
"""

def single_photo_details(photo_data, counter, user_name, profile_pic_small, profile_pic_large, flag):
    try:
        # ---------------------------------------------
        # Dumping the only necessary data in temporary variable
        # ---------------------------------------------
        photo_id = photo_data['id']
        created_at = photo_data['created_at']
        updated_at = photo_data['updated_at']
        color = photo_data['color']
        photo_width = photo_data['width']
        photo_height = photo_data['height']

        if flag==True:
            curated_photo_user = photo_data['user']['name']
            curated_photo_profile_small = photo_data['user']['profile_image']['small']
            curated_photo_profile_large = photo_data['user']['profile_image']['large']

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
        if flag==True:
            data = {
                'photo_id': photo_id, 'created_at': created_at, 'updated_at': updated_at, 'color': color,
                'photo_height': photo_height, 'photo_width': photo_width,
                'url_thumb': url_thumb, 'url_small': url_small, 'url_custom': url_custom,
                'url_raw': url_raw, 'url_full': url_full,
                'url_regular': url_regular, 'url_download': url_download, 'url_share': url_share,
                'user_display_name': curated_photo_user,
                'user_profile_pic': curated_photo_profile_large,
                'user_profile_pic_small': curated_photo_profile_small,
                'curated_id': user_name
            }
        else:
            data = {
                'photo_id': photo_id, 'created_at': created_at, 'updated_at': updated_at, 'color': color,
                'photo_height': photo_height, 'photo_width': photo_width,
                'url_thumb': url_thumb, 'url_small': url_small, 'url_custom': url_custom,
                'url_raw': url_raw, 'url_full': url_full,
                'url_regular': url_regular, 'url_download': url_download, 'url_share': url_share,
                'user_display_name': user_name,
                'user_profile_pic': profile_pic_large,
                'user_profile_pic_small': profile_pic_small
            }

        # ---------------------------------------------
        # check serialize validation and insert--------
        # ---------------------------------------------
        serialized_data = PhotoSerializer(data=data)

        if serialized_data.is_valid():
            try:
                photo_unique_id = serialized_data.save()
                print str(photo_unique_id.photo_id) + " ||success for|| "+ str(counter)
                if flag != True:
                    return photo_unique_id.photo_id
                else:
                    return True

            except IntegrityError as db_insert_error:
                print "Photo already exist with the same id: "+str(db_insert_error)
                if flag == True:
                    return False
                else:
                    return get_single_photo(photo_id)

        else:
            print " ||ERRor for|| " + str(counter)
            if flag == True:
                return False
            else:
                return get_single_photo(photo_id)

    except ValueError as error:
        print " ||ERRor for|| " + str(counter) + " error is "+ str(error)
        if flag == True:
            return False
        else:
            return get_single_photo(photo_id)


"""
-----------------------------------------------------------
-----------------------------------------------------------
functions take one parameter (photo_id) and get/return it to
Model (Photo) via Serializer.
@:photo_id -> current id of the photo.
@:return photo object id (photo_id, primary key of Photo) associate with the current photo id, if exist.
-----------------------------------------------------------
-----------------------------------------------------------
"""

def get_single_photo(photo_id):
    single_photo = Photo.objects.get(photo_id = str(photo_id))
    return single_photo.photo_id





"""
-----------------------------------------------------------
-----------------------------------------------------------
functions to add curated photos of a particular list in the database. handles the list with the basis of "How many photos a collection have"
handles curated collections list only
url: BASE_URL + /unsplash/add_collection?method=1&id=1234
method = 1 -> curated collections
method = 2 -> featured collections
id = 1234 (integer) -> contains id of associates curated/featured collections
-----------------------------------------------------------
-----------------------------------------------------------
"""


def add_collections_photo(req):
    if req.method == 'GET':
        collection_id = int(req.GET.get('id', "1"))
        current_method = int(req.GET.get('method', 1))

        total_photos = get_total_photos_curated(collection_id)
        current_page = 1
        total_page = int(total_photos) / 10
        success = 0
        failure = 0

        if total_page == 0:
            total_page = 1 #safe value, in case total photo is less than default loading

        print "for current method : "+str(current_method) + " < total page "+str(total_page) + " current page "+ str(current_page) + " for total photos "+str(total_photos)
        while (current_page <= 2):

            if current_method == 1:
                #this is curated url
                curated_photo_feed = requests.get(UNSPLASH_BASE_URL + 'collections/curated/'+str(collection_id)+'/photos/?client_id='+ BEYBLADE_ID + '&page=' + str(current_page))
            else:
                #this is featured collection
                curated_photo_feed = requests.get(UNSPLASH_BASE_URL + 'collections/' + str(
                    collection_id) + '/photos/?client_id=' + BEYBLADE_ID + '&page=' + str(current_page))

            curated_collection_photo = curated_photo_feed.json()
            for counter in range(0, len(curated_collection_photo)):
                try:
                    status_flag = single_photo_details(curated_collection_photo[counter], counter, str(collection_id), "", "", True)

                    if status_flag:
                        success += 1
                    else:
                        failure += 1
                except ValueError as error:
                    print " ||ERRor for|| " + str(counter) + " error is " + str(error)

            print "Current Method -> "+ str(current_method) +" Total Success: "+str(success) + " total failure "+str(failure) + " for page "+ str(current_page)
            current_page+= 1

        return HttpResponse("Hello Collections "+"%s%s\n"+"Current Method -> "+ str(current_method) + " success -> "+ str(success) + " failure -> "+str(failure))



"""
-----------------------------------------------------------
-----------------------------------------------------------
returns the total photos of a curated_list from the database
to add the photos as long as needed to complete the collection
collecting [curated]
-----------------------------------------------------------
-----------------------------------------------------------
"""
def get_total_photos_curated(curated_id):
    curated_object = CollectionList.objects.get(curated_id = str(curated_id))
    print "Get total photos of a curated list: "+str(curated_object.curated_total_photos)
    return curated_object.curated_total_photos


"""
-----------------------------------------------------------
-----------------------------------------------------------
handles the API call to fetch and return collection information
based on What USER needs
@url parameter -> method 1 -> curated, method 2 -> featured collection
-----------------------------------------------------------
-----------------------------------------------------------
"""
def get_collection(request):
    if request.method == 'GET':
        current_method = int(request.GET.get('method', 1))
        response_data = {}
        collection_data = []
        counter = 0

        if current_method == 1:
            latest_collection = CollectionList.objects.filter(curated_is_curated = True).order_by('-curated_id')
        elif current_method == 2:
            latest_collection = CollectionList.objects.filter(curated_is_featured=True).order_by('-curated_id')
        else:
            latest_collection = CollectionList.objects.filter(curated_is_curated = True).order_by('-curated_id')#safe check

        try:
            current_page = int(request.GET.get('page', "1"))
        except ValueError as error:
            current_page = 1
            print str(error)

        upper_limit = int(current_page * 10)
        lower_limit = int(upper_limit) - 10 + 1
        total = 0

        print "current method "+str(current_method) + " current page "+str(current_page)

        for entry in latest_collection:
            counter += 1

            if lower_limit <= counter <= upper_limit:
                # To check if description is none
                if entry.curated_description != None:
                    description =  unicodedata.normalize('NFKD',entry.curated_description).encode('ascii',
                                                                                                                   'ignore')
                else:
                    description = "none"
                # To check if description is none

                new_photo_data = {'collection_id': str(entry.curated_id),
                                  'collection_title': unicodedata.normalize('NFKD', entry.curated_title).encode('ascii',
                                                                                                                   'ignore'),
                                  'collection_description': description,
                                  'published': str(entry.curated_published),
                                  'updated': str(entry.curated_updated),

                                  'is_curated': str(entry.curated_is_curated),
                                  'is_featured': str(entry.curated_is_featured),
                                  'total_photos': str(entry.curated_total_photos),
                                  'user_name': str(entry.curated_user_name),
                                  'profile_image_small': str(entry.curated_profile_image_small),
                                  'profile_image_large': str(entry.curated_profile_image_large),

                                  'collection_url_self': str(entry.curated_collection_url_self),
                                  'collection_url_html': str(entry.curated_collection_url_html),

                                  'url_thumb': str(entry.curated_cover_photo.url_thumb),
                                  'url_small': str(entry.curated_cover_photo.url_small),
                                  'url_raw': str(entry.curated_cover_photo.url_raw),
                                  'url_full': str(entry.curated_cover_photo.url_full),
                                  'url_regular': str(entry.curated_cover_photo.url_regular),
                                  'url_custom': str(entry.curated_cover_photo.url_custom),

                                  'cover_color': str(entry.curated_cover_photo.color),
                                  'cover_height': str(entry.curated_cover_photo.photo_height),
                                  'cover_width': str(entry.curated_cover_photo.photo_width)
                                  }

                collection_data.append(new_photo_data)
                total += 1

        response_data['total'] = total
        response_data['collections'] = collection_data

        if current_method == 1:
            response_data['is_curated'] = True
        elif current_method == 2:
            response_data['is_featured'] = True

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        error_response = {'error': 'error occurred', 'message': 'unknown method'}
        return HttpResponse(json.dump(error_response), content_type='application/json')