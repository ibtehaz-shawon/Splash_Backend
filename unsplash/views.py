from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from unsplash.forms import SubmitEmbed
from unsplash.models import Photo
from django.core import serializers
import requests, json

# Create your views here.
from unsplash.serializer import EmbedSerializer

CLIENT_ID = 'badb97318ed82cec37d0fb85539b695a3d183a9ca6d2fd97bb4d10289b9ff0fe'

def index(req):
    r = requests.get('https://api.unsplash.com/photos/Ks2yANaNbHU?client_id='+CLIENT_ID)
    # serializer = EmbedSerializer(data=json)
    # photo_details = serializers.serialize("json", r.json())
    photoID = json.dumps(r.json())
    serialized_data = EmbedSerializer(data=photoID)
    if serialized_data.is_valid():
        return HttpResponse(serialized_data)
    else:
        return HttpResponse("Oh!")


def getFeed(req):
    latest_photos = Photo.objects.order_by('-created_at')[:10]
    output = serializers.serialize("json", latest_photos)
    return HttpResponse(output, content_type='application/json')
