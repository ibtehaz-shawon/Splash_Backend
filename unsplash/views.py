from django.http import HttpResponse
from django.shortcuts import render
from unsplash.models import Photo
from django.core import serializers

# Create your views here.
def index(request):
    # Task.objects.all
    return HttpResponse("Hello World")


def getFeed(request):
    latest_photos = Photo.objects.order_by('-created_at')[:10]
    output = serializers.serialize("json", latest_photos)
    return HttpResponse(output, content_type='application/json')
