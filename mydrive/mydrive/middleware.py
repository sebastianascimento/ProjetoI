# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class CustomLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.user.is_superuser:
                if request.path.startswith(reverse('admin:index')):
                    return response
                return redirect('/admin/')
            elif request.user.is_staff:
                if request.path.startswith('/admin/'):
                    return response  
                else:
                    return redirect('/admin/')  
            elif request.path.startswith(reverse('foldermaster:foldermanagement')):
                return response

        return response
