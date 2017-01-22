from rest_framework import serializers
from .models import Photo

class EmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        # Nested Serializer
        # http: // www.django - rest - framework.org / api - guide / serializers /
        fields = ('id', 'created_at', 'color', )

# class UserSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     username = serializers.CharField(max_length=100)
#
# class CommentSerializer(serializers.Serializer):
#     user = UserSerializer(required=False)
#     edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
#     content = serializers.CharField(max_length=200)
#     created = serializers.DateTimeField()
