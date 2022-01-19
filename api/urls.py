from django.urls import path
from . import views

urlpatterns = [
    path('drafts/', views.DraftList.as_view()),
    path('albums/', views.AlbumList.as_view()),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view()),
]
