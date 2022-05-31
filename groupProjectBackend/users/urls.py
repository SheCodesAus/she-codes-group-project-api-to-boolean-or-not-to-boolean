from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('users/logout/', views.SheCodesUserLogout.as_view()),
    path('', views.SheCodesUserList.as_view()),
    path('<int:pk>/', views.SheCodesUserDetail.as_view()),
    path('authenticate/', views.CustomObtainAuthToken.as_view()),
    path('shecodes-user-list/', views.SuperUserOrAdminSheCodesUsernameList.as_view()),
    path('shecodes-user-list/<int:pk>/', views.SheCoderDataPermissions.as_view()),
    path('<int:pk>/superuser/add-auth-level/', views.UpdateToAdminOrApproverUserView.as_view()),
    path('<int:pk>/admin-add-approver/', views.ChangeUsertoApproverView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)