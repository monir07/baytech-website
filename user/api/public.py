import jwt

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
# Email Validation Works related Imports
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.response import Response

from base.helpers.token_generator import create_tokens
from user.serializers import (
    RegisterSerializer, 
    ResetPasswordRequestSerializer, 
    ResetPasswordAcceptSerializer, 
    SignInSerializer, 
    RefreshTokenSerializer,
    AccountActiveSerializer
)
User = get_user_model()


class RegisterUserAPIView(CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

  def perform_create(self, serializer):
        user = serializer.save(is_active = False)
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('user/acc_active_api.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = serializer.validated_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()


class AccountActiveAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AccountActiveSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uidb64 = serializer.validated_data.get('uid')
            token = serializer.validated_data.get('token')
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User._default_manager.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
                response = {
                    "Success": False,
                    "Message": "User not found with this UID!"
                }
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            token_checked = default_token_generator.check_token(user, token)
            if not token_checked:
                response = {
                    "Success": False,
                    "Message": "Token didn't matched for this User! Or token is used or expired!"
                }
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if user is not None and token_checked:
                user.is_active = True
                user.save()
                response = {
                    "Success": True,
                    "Message": "User activated!"
                }
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            try:
                user = User.objects.get(username__exact=username)
                if not user.is_active:
                    raise ValidationError(detail='User Inactive', code=status.HTTP_400_BAD_REQUEST)
                if not user.check_password(raw_password=password):
                    raise ValidationError(detail='invalid password', code=status.HTTP_400_BAD_REQUEST)
                access_token, refresh_token = create_tokens(user=user)
                data = {
                    'access': access_token,
                    'refresh': refresh_token,
                }
                return Response(data=data, status=status.HTTP_201_CREATED)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                raise ValidationError(detail='user not found', code=status.HTTP_404_NOT_FOUND)


class RefreshTokenAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RefreshTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            refreshed_token = serializer.validated_data.get('refresh')
            try:
                payload = jwt.decode(jwt=refreshed_token, key=settings.SECRET_KEY, algorithms='HS256', verify=True)
                if payload['token_type'] != 'refresh':
                    return Response({'message': 'This is not a correct refresh token!', 'success': False}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                user_obj = get_object_or_404(User, username=payload.get('username'), is_active=True)
                access_token, refresh_token = create_tokens(user=user_obj)
                return Response({'access': access_token, 'refresh': refresh_token}, status=status.HTTP_201_CREATED)
            except Exception as err:
                return Response({'message': f'{str(err)}', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordRequestAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            domain = serializer.validated_data.get('domain')
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({
                    "success":False,
                    "message": "No user found with this email!"
                }, status=status.HTTP_404_NOT_FOUND)
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('user/password_reset_email.html', {
                'user': user,
                'domain': domain or current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
        headers = self.get_success_headers(serializer.data)
        response = serializer.data
        response.update({
            "Message": "An email is sent to this email. Please check there and come on password reset accept view!!"
        })
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
    

class ResetPasswordAcceptAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordAcceptSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uidb64 = serializer.validated_data.get('uid')
            token = serializer.validated_data.get('token')
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User._default_manager.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
                response = {
                    "Success": False,
                    "Message": "User not found with this UID!"
                }
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            token_checked = default_token_generator.check_token(user, token)
            if not token_checked:
                response = {
                    "Success": False,
                    "Message": "Token didn't matched for this User! Or token is used or expired!"
                }
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if user is not None and token_checked:
                user.set_password(serializer.validated_data.get("password"))
                user.save()
                response = {
                    "Success": True,
                    "Message": "Password Reset Done!"
                }
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data, status=status.HTTP_201_CREATED)