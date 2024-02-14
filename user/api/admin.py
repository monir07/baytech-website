from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from base.permissions import IsSuperUser, IsStaff
from user.serializers import UserCreateSerializer, UserSerializer
from base.helpers.decorators import exception_handler
from base.exceptions import UnprocessableEntity
from user.models import User
from base.helpers.func import entries_to_remove
from django.core.mail import EmailMultiAlternatives


class AdminUserListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser))
    queryset = User.objects.filter()
    serializer_class = UserSerializer
    search_fields = ['username', 'first_name', 'last_name']
    filterset_fields = ['is_active', 'is_staff', 'type']


@api_view(['POST'])
@permission_classes([IsAuthenticated, (IsStaff | IsSuperUser)])
@exception_handler
def create_user(request: Request) -> Response:
    email = request.data['email']
    try:
        User.objects.get(username=email)
        raise UnprocessableEntity(detail='username with this email already exists!', code=status.HTTP_406_NOT_ACCEPTABLE)
    except User.DoesNotExist:
        user = User()
        user.username = email
        user.set_password(raw_password=request.data['password'])
        user.is_staff = request.data.get('is_staff', False)
        user.is_active = request.data.get('is_active', True)
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.email = email
        user.save()
        msg = EmailMultiAlternatives("New Account Created on core", f"An account Created on core app with This email. Please login with this email and password : {request.data['password']}", to=[request.data['email']])
        msg.send(fail_silently=False)
        return Response(data={'data': UserSerializer(user).data}, status=status.HTTP_201_CREATED)



class AdminUserListCreateApiView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser))
    serializer_class = UserCreateSerializer
    queryset = User.objects.filter(is_superuser=False)

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['username'] = request.data['email']
        request.data['password'] = make_password('default')
        return super(AdminUserListCreateApiView, self).create(request, *args, **kwargs)


class AdminUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser))
    serializer_class = UserCreateSerializer
    queryset = User.objects.filter(is_superuser=False)
    http_method_names = ['patch', 'get']
    lookup_field = 'pk'
    removeable_keys = ('username', 'email', 'is_superuser', 'is_stuff', 'password', 'groups', 'user_permissions')

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        self.request.data.update(entries_to_remove(self.request.data, self.removeable_keys))
        return super(AdminUserRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)
        

class UserProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser))
    serializer_class = UserSerializer
    queryset = User.objects.filter()
    http_method_names = ['patch', 'get']
    removeable_keys = ('username', 'email','type','is_superuser', 'is_active', 'is_stuff', 'verified', 'password', 'groups', 'user_permissions')
    
    def get_object(self):
        return  self.request.user

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        self.request.data.update(entries_to_remove(self.request.data, self.removeable_keys))
        return super().patch(request, *args, **kwargs)
