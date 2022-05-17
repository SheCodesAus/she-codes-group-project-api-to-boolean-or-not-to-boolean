from unicodedata import category
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.pagination import LimitOffsetPagination

from .models import StickyNote
from .serializers import StickyNoteSerializer
from django.http import Http404
from rest_framework import status, permissions
# from .permissions import IsOwnerOrReadOnly


# Create your views here.


# create sticky notes, need to check this still allows create without  

class StickyNote(APIView):

    def post(self, request):
        serializer = StickyNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )