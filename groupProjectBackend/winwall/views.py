from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth.models import AnonymousUser
from .models import Collection, WinWall, StickyNote
from .serializers import WinWallSerializer, WinWallDetailSerializer, StickyNoteDetailSerializer, StickyNoteSerializer, CollectionSerializer, CollectionDetailSerializer, AdminStickyNoteDetailSerializer, WinWallBulkUpdateSerializer
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly, IsSuperUserOrAdmin, WinWallOwnerWritePermission, IsSuperUserOrAdminOrApprover

class AdminWinWallList(APIView):
    # SuperUser, Admin / Approver can get and post to the list of the WinWalls
    permission_classes = [
        IsSuperUserOrAdmin
        ]

    def get(self, request):
        win_walls = WinWall.objects.all()
        serializer = WinWallSerializer(win_walls, many=True)
        return Response(serializer.data)

    # SuperUser, Admin / Approver can post new WinWalls
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

class AdminWinWallDetailView(APIView):
    # SuperUser, Admin or Approver of the WinWall can get, edit and delete
    permission_classes = [
        WinWallOwnerWritePermission, IsSuperUserOrAdminOrApprover
        ]

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

    # admin / approver can edit WinWalls
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

    # admin / approver can delete WinWalls
    def delete(self, request, pk):
        win_wall = self.get_object(pk)
        win_wall.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SheCoderWinWallList(APIView):
    # Everyone who is logged in or out can get entire list of previous WinWalls
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        ]

    def get(self, request):
        win_walls = WinWall.objects.all()
        serializer = WinWallSerializer(win_walls, many=True)
        return Response(serializer.data)

class SheCoderWinWallDetailView(APIView):
    # any user accessing the website can getview WinWalls
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        ]

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

class WinWallBulkUpdate(APIView):
    permission_classes = [IsSuperUserOrAdmin]

    def get_object(self, pk):
        try:
            win_wall_sticky_notes = StickyNote.objects.filter(win_wall_id=pk)
            return win_wall_sticky_notes

        except WinWall.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        win_wall_sticky_notes = self.get_object(pk)
        data = request.data
        serializer = WinWallBulkUpdateSerializer(
            data = data,
          
        )

        if serializer.is_valid():
            approve = serializer.validated_data.get('bulk_approve')
            archive = serializer.validated_data.get('bulk_archive')
            for note in win_wall_sticky_notes:
                if approve != None:
                    note.is_approved = approve
                if archive != None:
                    note.is_archived = archive
                note.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectionList(APIView):
    permission_classes = [IsSuperUserOrAdmin]

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
        
class SheCoderCollectionList(APIView):
    # Everyone who is logged in or out can get entire list of Collections
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        ]

    def get(self, request):
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)

class CollectionDetail(APIView):
    permission_classes = [IsSuperUserOrAdmin]

    def get_object(self, pk):
        try:
            collections = Collection.objects.get(pk=pk)
            self.check_object_permissions(self.request,collections)
            return collections

        except Collection.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        collections = self.get_object(pk)
        serializer = CollectionDetailSerializer(collections)
        return Response(serializer.data)
      
    def put(self, request, pk):
        collections = self.get_object(pk)
        data = request.data
        serializer = CollectionDetailSerializer(
            instance=collections,
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
        collections = self.get_object(pk)
        collections.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      
class StickyNoteList(APIView):
    # guests and logged in users can post new sticky-notes
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

class AdminStickyNoteDetail(APIView):
    # sticky notes can only be approved or archved by admin 
    permission_classes = [
        IsSuperUserOrAdminOrApprover
        ]
    
    def get_object(self, pk):
        try:
            stickynote = StickyNote.objects.get(pk=pk)
            self.check_object_permissions(self.request, stickynote)
            return stickynote
        except StickyNote.DoesNotExist:
            raise Http404 

    def get(self, request, pk):
        stickynote = self.get_object(pk)
        serializer = AdminStickyNoteDetailSerializer(stickynote)
        return Response(serializer.data)

    def put(self, request, pk):
        stickynote = self.get_object(pk)
        data = request.data
        serializer = AdminStickyNoteDetailSerializer(
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

class StickyNoteDetail(APIView):
    # sticky notes can only be approved or archved by admin 
    permission_classes = [
        IsOwnerOrReadOnly
        ]
    
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