from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Album, Tag
from .serializers import AlbumSerializer, ImageSerializer, TagSerializer


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


class AlbumList(APIView):
    """
    List all existing albums of a user, or create a new album.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        albums = Album.objects.filter(owner=request.user)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlbumSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlbumDetailView(APIView):
    """
    Retrieve, update or delete an album instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Album.objects.get(pk=pk)
        except Album.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        album = self.get_object(pk)
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    def put(self, request, pk):
        album = self.get_object(pk)
        serializer = AlbumSerializer(
            album, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        album = self.get_object(pk)
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
