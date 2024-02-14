import logging
import jwt
from typing import List, Dict
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework import exceptions, status
logger = logging.getLogger('django')
User = get_user_model()


class DetailDictMixin:
    def __init__(self, detail=None, code=None):
        detail_dict = {"detail": self.default_detail, "code": self.default_code}

        if isinstance(detail, dict):
            detail_dict.update(detail)

        elif detail is not None:
            detail_dict["detail"] = detail

        if code is not None:
            detail_dict["code"] = code

        super().__init__(detail_dict)


class AuthenticationFailed(DetailDictMixin, exceptions.AuthenticationFailed):
    pass


class InvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Token is invalid or expired")
    default_code = "token_not_valid"


class CustomTokenAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate_header(self, request):
        return '{} realm="{}"'.format(
            "Bearer",
            self.www_authenticate_realm,
        )
    
    def authenticate(self, request):
        auth_header: str = request.headers.get('authorization')
        if auth_header:
            token_obj: List[str] = auth_header.split(' ')
            if token_obj[0].lower() != 'bearer':
                return None
            try:
                payload: Dict = jwt.decode(jwt=token_obj[1], key=settings.SECRET_KEY, algorithms='HS256', verify=True)
                if payload['token_type'] != 'access':
                    return None
                user_obj = self.get_user(payload)
                if not user_obj:
                    return None
                return user_obj, payload
            except Exception as err:
                return None

    def get_user(self, validated_token):
        try:
            user_id = validated_token["username"]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))
        try:
            user = self.user_model.objects.get(**{"username": user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")
        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
        return user
