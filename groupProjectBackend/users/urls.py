# users/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# adding log out URL 
urlpatterns = [

    path('users/logout/', views.CustomUserLogOut.as_view()),

    
]

urlpatterns = format_suffix_patterns(urlpatterns)