from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def staff_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'staff':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'user':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def user_not_staff(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'user':
            return function(request, *args, **kwargs)
        else:
            return redirect('/admin/')
    return wrap
