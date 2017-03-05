from rest_framework import serializers
from .models import Photo, CuratedList


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'



class CuratedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuratedList
        fields = '__all__'