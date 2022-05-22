from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # admin only view
    path('admin-win-walls/', views.AdminWinWallList.as_view()),
    # general user view
    path('win-walls/', views.SheCoderWinWallList.as_view()),
    # admin only view
    path('admin-win-wall/<int:pk>/', views.AdminWinWallDetailView.as_view()),
    # general user view
    path('win-wall/<int:pk>/', views.SheCoderWinWallDetailView.as_view()),
    # general users & admins view
    path('sticky-notes/', views.StickyNoteList.as_view()),
    # admin only view
    path('sticky-note/<int:pk>/', views.StickyNoteDetail.as_view()),
    # in progress - bulk updates of SN via winwall 
    path('win-wall-notes/<int:pk>/', views.WinWallBulkUpdate.as_view()),
    
    path('collections/', views.CollectionList.as_view()),
    path('collection/<slug:slug>/', views.CollectionDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)