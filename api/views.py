from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Album, Image, Relationship, Tag
from .serializers import AlbumSerializer, ImageSerializer, TagSerializer
from api import serializers


class Discover(APIView):
    '''
    Returns albums associated with tags used by the user
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tags = set()
        albums = Album.objects.filter(owner=request.user, is_published=True)
        recommanded_albums = None
        for album in albums:
            for tag in album.tags.all():
                tags.add(tag.title)
        recommanded_albums = Album.objects.filter(
            tags__title__in=tags).distinct()
        serializer = AlbumSerializer(recommanded_albums, many=True)
        return Response(serializer.data)


class FollowToggle(APIView):
    '''
    Follow or Unfollow Someone
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # user which we want to follow
            following = User.objects.get(pk=request.data.get('user_id'))
            follower = request.user

            if Relationship.objects.filter(follower=follower, followed=following).exists():
                # unfollow
                obj = Relationship.objects.get(
                    follower=follower, followed=following)
                obj.delete()
                return Response({"message": "Stopped following"})
            else:
                newFollower = Relationship.objects.create(
                    follower=follower, followed=following)
                newFollower.save()
                return Response({"message": "Started following"})
        except User.DoesNotExist:
            return Response({"message": "User doesn't exist"})


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


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_class = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(owner=user)


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

        album_obj.images.clear()
        for image in data.get('images'):
            try:
                image_obj = Image.objects.get(pk=image.get('id'))
            except Image.DoesNotExist:
                # create new image object
                image_obj = Image.objects.create(
                    caption=image.get('caption'),
                    caption_color=image.get('caption_color'),
                    caption_position=image.get('caption_position'),
                    source=image.get('source'),
                    owner=request.user
                )
                image_obj.save()
            album_obj.images.add(image_obj)

        album_obj.save()
        serializer = AlbumSerializer(album_obj)

        return Response(serializer.data)
