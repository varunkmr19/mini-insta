from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Album, Image, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Album
        fields = '__all__'
