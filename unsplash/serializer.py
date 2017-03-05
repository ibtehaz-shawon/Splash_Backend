from rest_framework import serializers
from .models import Photo, CollectionList


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'



class CuratedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionList
        fields = '__all__'