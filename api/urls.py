from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register(r'albums', views.AlbumViewSet, basename='albums')
router.register(r'tags', views.TagViewSet, basename='tags')

# urlpatterns = [
#     path('drafts/', views.DraftList.as_view()),
#     path('albums/', views.AlbumList.as_view()),
#     path('albums/<int:pk>/', views.AlbumDetailView.as_view()),
# ]

urlpatterns = router.urls
