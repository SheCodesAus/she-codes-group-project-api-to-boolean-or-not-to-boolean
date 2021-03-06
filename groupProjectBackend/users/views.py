from django.http import Http404
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import logout 
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from .models import SheCodesUser
from .serializers import SheCodesUserSerializer, SheCodesUserDetailSerializer, ViewSheCodesUserSerializer, MakeUserAdminOrApproverDetailSerializer, ChangeUserToApproverDetailSerializer, DisplaySheCodesUsernameDetailSerializer, NameAndPermissionDataDetailSerializer
from .permissions import IsSuperUser, IsSuperUserOrAdmin, IsOwnerOrReadOnly

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})

class SheCodesUserLogout(APIView):
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

class SheCodesUserList(APIView):
    permission_classes = [permissions.AllowAny,]
    queryset = SheCodesUser.objects.all()

    def get(self, request):
        users = SheCodesUser.objects.all()
        serializer = ViewSheCodesUserSerializer(users, many=True)
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

# Displays Full List of Users - their ID & Username
class SuperUserOrAdminSheCodesUsernameList(APIView):
    permission_classes = [IsSuperUserOrAdmin]
    queryset = SheCodesUser.objects.all()

    def get(self, request):
        users = SheCodesUser.objects.all()
        serializer = DisplaySheCodesUsernameDetailSerializer(users, many=True)
        return Response(serializer.data)

# Displays the permission data for User associated with the selected ID from the React drop-down
class SheCoderDataPermissions(APIView):
    permission_classes = [IsSuperUserOrAdmin]

    def get_object(self, pk):
        try:
            return SheCodesUser.objects.get(pk=pk)
        except SheCodesUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = NameAndPermissionDataDetailSerializer(user)
        return Response(serializer.data)

class SheCodesUserDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Authorisation Views:
# Super User can make someone an Admin or an Approver
class UpdateToAdminOrApproverUserView(APIView):
    # This view only allows the SuperUsers to make a User an Admin or Approver
    permission_classes = [IsSuperUser]
    def get_object(self, pk):
        try:
            return SheCodesUser.objects.get(pk=pk)
        except SheCodesUser.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = MakeUserAdminOrApproverDetailSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsertoApproverView(APIView):
    # This view allows an Admin or the SuperUser to make a general user an approver
    permission_classes = [IsSuperUserOrAdmin]
    def get_object(self, pk):
        try:
            return SheCodesUser.objects.get(pk=pk)
        except SheCodesUser.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = ChangeUserToApproverDetailSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
