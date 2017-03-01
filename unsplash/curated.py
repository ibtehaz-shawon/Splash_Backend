from django.contrib.sites import requests
from django.http import HttpResponse
import requests
import json

from unsplash_backend.settings import BEYBLADE_ID, UNSPLASH_BASE_URL


page_number = 1 #default

def get_curated_list(req):

    if req.method == 'GET':
        curated_feed = requests.get(UNSPLASH_BASE_URL + 'collections/curated/?client_id='
                                    + BEYBLADE_ID + '&page=' + str(1))
        try:
            feed_array = curated_feed.json()
            # print feed_array[0]['id']
            return HttpResponse(feed_array)
        except ValueError as error:
            print "No JSON file " + str(error)
            return HttpResponse(str(error))