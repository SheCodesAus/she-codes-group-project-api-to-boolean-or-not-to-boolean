from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WinWall
from. serializers import WinWallSerializer, WinWallDetailSerializer
# from rest_framework import status, permissions, generics
# from .permissions import IsOwnerorReadOnly


class WinWallList(APIView):
    
    # I can see the winwall list when loged off but I can't post/create a project unless logged in.
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        winwalls = WinWall.objects.all()
        serializer = WinWallSerializer(winwalls, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = WinWallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

class WinWallDetail(APIView):

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerorReadOnly]

    def get_object(self, pk):
        try:
            winwall = WinWall.objects.get(pk=pk)
            self.check_object_permissions(self.request,winwall)
            return winwall

        except WinWall.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        winwall = self.get_object(pk)
        serializer = WinWallDetailSerializer(winwall)
        return Response(serializer.data)

    def put(self, request, pk):
        winwall = self.get_object(pk)
        data = request.data
        serializer = WinWallDetailSerializer(
            instance = winwall,
            data = data,
            partial = False
        )
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

