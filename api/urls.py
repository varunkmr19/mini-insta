from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register(r'albums', views.AlbumViewSet, basename='albums')
router.register(r'tags', views.TagViewSet, basename='tags')
router.register(r'images', views.ImageViewSet, basename='images')

urlpatterns = [
    path('drafts/', views.DraftList.as_view()),
    path('discover/', views.Discover.as_view())
]

urlpatterns += router.urls
