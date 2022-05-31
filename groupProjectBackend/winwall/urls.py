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
    # in progress - bulk updates of SN via winwall 
    path('win-wall-notes/<int:pk>/', views.WinWallBulkUpdate.as_view()),
    # general users & admins view
    path('sticky-notes/', views.StickyNoteList.as_view()),
    # admin only view
    path('admin-sticky-note/<int:pk>/', views.AdminStickyNoteDetail.as_view()),
    path('sticky-note/<int:pk>/', views.StickyNoteDetail.as_view()),
    # in progress - bulk updates of SN via winwall 
    path('win-wall-notes/<int:pk>/', views.WinWallBulkUpdate.as_view()),
    # general users can view the list of collections
    path('view-collections/', views.SheCoderCollectionList.as_view()),
    # admin / approver level only access for collections
    path('collections/', views.CollectionList.as_view()),
    # admin / approver level only access for collection ID
    path('admin-collection/<int:pk>/', views.AdminCollectionDetail.as_view()),
    # any user can view collection by ID
    path('collection/<int:pk>/', views.SheCoderCollectionDetail.as_view()),
    path('assignments/', views.UserAssignmentList.as_view()),
    path('assignment/<int:pk>/', views.UserAssigmentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)