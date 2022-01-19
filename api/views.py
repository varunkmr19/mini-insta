from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Album, Tag
from .serializers import AlbumSerializer, ImageSerializer, TagSerializer
from api import serializers


class DraftList(APIView):
    '''
    List all albums of the user that are not published.
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        unpublished_albums = Album.objects.filter(
            owner=request.user, is_published=False)
        serializer = AlbumSerializer(unpublished_albums, many=True)
        return Response(serializer.data)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_class = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        data = request.data
        album = Album.objects.create(name=data.get('name'), owner=request.user)
        album.save()

        for tag in data.get('tags'):
            try:
                tag_obj = Tag.objects.get(title=tag.get('title'))
            except Tag.DoesNotExist:
                # create new tag
                tag_obj = Tag.objects.create(
                    title=tag.get('title')
                )
                tag_obj.save()

            album.tags.add(tag_obj)

        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        album_obj = self.get_object()
        data = request.data

        album_obj.name = data.get('name')
        album_obj.owner = request.user

        album_obj.tags.clear()
        for tag in data.get('tags'):
            try:
                tag_obj = Tag.objects.get(title=tag.get('title'))
            except Tag.DoesNotExist:
                # create new tag
                tag_obj = Tag.objects.create(
                    title=tag.get('title')
                )
                tag_obj.save()

            album_obj.tags.add(tag_obj)

        album_obj.save()
        serializer = AlbumSerializer(album_obj)

        return Response(serializer.data)
