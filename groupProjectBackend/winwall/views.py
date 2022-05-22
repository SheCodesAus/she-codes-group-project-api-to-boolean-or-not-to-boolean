from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Collection, WinWall, StickyNote
from .serializers import WinWallSerializer, WinWallDetailSerializer, StickyNoteSerializer, CollectionSerializer, CollectionDetailSerializer
from unicodedata import category
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly

# from .permissions import IsOwnerorReadOnly

class CollectionList(APIView):

    def get(self, request):
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
 
    def post(self,request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id = request.user)
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
        
class CollectionDetail(APIView):
    
    def get(self, request):
        collections = CollectionDetail.objects.all()
        serializer = CollectionDetailSerializer(collections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CollectionDetailSerializer(data=request.data)
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


class WinWallList(APIView):
    
    # I can see the winwall list when loged off but I can't post/create a project unless logged in.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        win_walls = WinWall.objects.all()
        serializer = WinWallSerializer(win_walls, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = WinWallSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            serializer.save(owner = request.user)
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

class WinWallDetail(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            win_wall = WinWall.objects.get(pk=pk)
            self.check_object_permissions(self.request,win_wall)
            return win_wall

        except WinWall.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        win_wall = self.get_object(pk)
        serializer = WinWallDetailSerializer(win_wall)
        return Response(serializer.data)

    def put(self, request, pk):
        win_wall = self.get_object(pk)
        data = request.data
        serializer = WinWallDetailSerializer(
            instance = win_wall,
            data = data,
            partial = True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# create sticky notes, need to check this still allows create without  

class StickyNoteList(APIView):

    def get(self, request):
        stickynotes = StickyNote.objects.all()
        serializer = StickyNoteSerializer(stickynotes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StickyNoteSerializer(data=request.data)
        if serializer.is_valid():
            if(not(type(request.user) is AnonymousUser)):
                serializer.save(owner=request.user)
            else:
                serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class StickyNoteDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]
    
    def get_object(self, pk):
        try:
            stickynote = StickyNote.objects.get(pk=pk)
            self.check_object_permissions(self.request, stickynote)
            return stickynote
        except StickyNote.DoesNotExist:
            raise Http404 

    def get(self, request, pk):
        stickynote = self.get_object(pk)
        serializer = StickyNoteDetailSerializer(stickynote)
        return Response(serializer.data)

    def put(self, request, pk):
        stickynote = self.get_object(pk)
        data = request.data
        serializer = StickyNoteDetailSerializer(
            instance=stickynote,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
                )
        return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stickynote = self.get_object(pk)
        stickynote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WinWallBulkUpdate(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]


    def get_object(self, pk):
        try:
            win_wall_sticky_notes = StickyNote.objects.filter(win_wall_id=pk)
            # self.check_object_permissions(self.request,win_wall_sticky_notes)
            return win_wall_sticky_notes

        except WinWall.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        win_wall_sticky_notes = self.get_object(pk)
        data = request.data
        serializer = WinWallBulkUpdateSerializer(
            instance = win_wall_sticky_notes,
            data = data,
            partial = True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)