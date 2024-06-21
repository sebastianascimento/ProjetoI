# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class CustomLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                # Superusuário ou staff acessa o admin
                if request.path.startswith(reverse('admin:index')):
                    return response
                return redirect('/admin/')
            else:
                # Usuário normal é redirecionado para a área de gerenciamento de pastas
                if request.path.startswith('/admin/'):
                    return redirect(reverse('foldermaster:foldermanagement'))
                elif request.path.startswith(reverse('foldermaster:foldermanagement')):
                    return response
                return redirect(reverse('foldermaster:foldermanagement'))

        return response
