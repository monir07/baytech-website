from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.serializers import UserSerializer, ChangePasswordSerializer
User = get_user_model()


class AdminUserProfileAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data.get('old_password')):
                return Response({"old_password": ["Old password didn't match!"]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data.get("password"))
            user.save()
            response = {
                'success':True,
                'message': 'Password updated successfully!',
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
