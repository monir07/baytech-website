from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response

def exception_handler(func):
    def inner_function(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except KeyError as ex:
            return Response({ex.__str__().strip("'"): ["This Field Is Required"]}, status=status.HTTP_400_BAD_REQUEST)
        except (ObjectDoesNotExist, Http404) as ex:
            return Response({'message': ex.__str__()}, status=status.HTTP_404_NOT_FOUND)
    return inner_function


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):  # allowed user by user group.
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            global group_name
            group = None
            if request.user.groups.exists():
                # group = request.user.groups.all()[1].name
                group = request.user.groups.all()
                for group_name in group:
                    name = group_name.name
                    if name in allowed_roles:
                        return view_func(request, *args, **kwargs)
                return redirect('403')
            return redirect('403')
                # return HttpResponse('You are not authorized to view this page')

        return wrapper_func

    return decorator


def allowed_by_user(allowed_roles=[]):  # allowed user by user.
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user:
                name = request.user.username
                if name in allowed_roles:
                    return view_func(request, *args, **kwargs)
                return redirect('403')
                # return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator