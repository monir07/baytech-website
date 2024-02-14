from django.urls import path, include
from user.api.admin import *
from user.api.user import *
from user.api.public import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authtoken.views import obtain_auth_token


admin_urls = [
    path('users/', AdminUserListAPIView.as_view(), name='admin-user-list'),
    path('create-user/', create_user, name='admin-user-create'),
    # path('create-user', AdminUserListCreateApiView.as_view(), name='admin-user-create'),
    path('update-user/<int:pk>/',
         AdminUserRetrieveUpdateAPIView.as_view(), name='admin-user-update'),
    path('update-profile/', UserProfileRetrieveUpdateAPIView.as_view(),
         name='user-profile-update'),
]

public_urls = [
    path('register/', RegisterUserAPIView.as_view(), name='user-registration-api'),
    path('register/active/', AccountActiveAPIView.as_view(), name='user-activation-api'),

    path('login/', obtain_auth_token, name='user-login-api'),
    path('login/token/', LoginAPIView.as_view(), name='user-login-api'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='user-token-refresh-api'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('reset_password/request/', ResetPasswordRequestAPIView.as_view(), name='user-token-refresh-api'),
    path('reset_password/accept/',ResetPasswordAcceptAPIView.as_view(),name="activate"),
]

authenticated_user_urls = [
    path('profile/', AdminUserProfileAPIView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password')
]

urlpatterns = [
    path('public/', include(public_urls)),
    path('user/', include(authenticated_user_urls)),
    path('admin/', include(admin_urls)),
]
