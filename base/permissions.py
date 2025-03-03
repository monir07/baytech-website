import copy
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()


class IsSuperUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_superuser

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        pass
        # return request.user == User.objects.get(pk=view.kwargs['id'])



class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

class CustomDjangoModelPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class HasRequiredPermissionForMethod(BasePermission):
    get_permission_required = None
    put_permission_required = None
    post_permission_required = None
    patch_permission_required = None
    delete_permission_required = None

    def has_permission(self, request, view):
        permission_required_name = f'{request.method.lower()}_permission_required'
        if not request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return False
        if not hasattr(view, permission_required_name):
            view_name = view.__class__.__name__
            self.message = f'IMPLEMENTATION ERROR: Please add the {permission_required_name} variable in the API view class: {view_name}.'
            return False

        permission_required = getattr(view, permission_required_name)
        if isinstance(permission_required, str):
            perms = [permission_required]
        else:
            perms = permission_required
        if not any(request.user.has_perm(perm) for perm in perms):
            self.message = f'Access denied. You need the/any_of {permission_required} permission to access this service with {request.method}.'
            return False
        # if not request.user.has_perm(permission_required):
        #     self.message = f'Access denied. You need the {permission_required} permission to access this service with {request.method}.'
        #     return False
        return True