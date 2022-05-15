from django.shortcuts import render

# Create your views here.
# pre adding imports based on what i used during prev project

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import CustomUser
from django.contrib.auth import logout 
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


# Define get and post users here




# Log out

class CustomUserLogOut(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)

        return Response({"success": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)