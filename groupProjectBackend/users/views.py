from .models import SheCodesUser
from .serializers import SheCodesUserSerializer, SheCodesUserDetailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})

class SheCodesUserList(APIView):
    permission_classes = [permissions.AllowAny,]
    queryset = SheCodesUser.objects.all()

    def get(self, request):
        users = SheCodesUser.objects.all()
        serializer = SheCodesUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SheCodesUserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user = serializer.data['id']
            token, created = Token.objects.get_or_create(user_id=user)
            return Response({
                'token': token.key,
                'data': serializer.data
            })
        return Response(serializer.errors)

class SheCodesUserDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ]

    def get_object(self, pk):
        try:
            return SheCodesUser.objects.get(pk=pk)
        except SheCodesUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = SheCodesUserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = SheCodesUserDetailSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)