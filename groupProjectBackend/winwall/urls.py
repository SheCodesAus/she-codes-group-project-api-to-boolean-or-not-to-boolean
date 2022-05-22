from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('win-walls/', views.WinWallList.as_view()),
    path('win-wall/<int:pk>/', views.WinWallDetail.as_view()),
    path('sticky-note/', views.StickyNoteList.as_view()),
    path('sticky-note/<int:pk>/', views.StickyNoteDetail.as_view()),
    # in progress - bulk updates of SN via winwall 
    path('win-wall-notes/<int:pk>/', views.WinWallBulkUpdate.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)