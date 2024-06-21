import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .models import Folder, File
from .forms import FolderForm, FileForm
from .forms import FileUploadForm 
from django.http import HttpResponse , Http404 , HttpResponseBadRequest , JsonResponse
from django.db.models import Sum
from django.contrib.auth import get_user_model
import zipfile
import logging


logger = logging.getLogger(__name__)


@login_required
def foldermanagement(request, folder_id=None):
    context = {}
    folders = None
    files = None
    folder = None
    breadcrumbs = []

    try:
        # Verifica e cria a pasta padrão se não existir
        if not Folder.objects.filter(owner=request.user).exists():
            default_folder = Folder.objects.create(name='Default Folder', owner=request.user)
            folder_id = default_folder.id

        # Calcula o espaço utilizado pelo usuário
        storage_used = sum(file.file.size for file in File.objects.filter(owner=request.user))
        print("Storage used:", storage_used)

        # Define o limite de armazenamento (50 MB neste exemplo)
        storage_limit = 50 * 1024 * 1024
        storage_available = storage_limit - storage_used
        context['storage_available'] = storage_available
        print("Storage available:", storage_available)

        if folder_id:
            folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
            folders = Folder.objects.filter(owner=request.user, parent=folder)
            files = File.objects.filter(owner=request.user, folder=folder)
            breadcrumbs = get_breadcrumbs(folder)
        else:
            folders = Folder.objects.filter(owner=request.user, parent=None)
            files = File.objects.filter(owner=request.user, folder=None)

        context.update({
            'folders': folders,
            'files': files,
            'folder': folder,
            'breadcrumbs': breadcrumbs,
        })

        # Processa submissões de formulários POST
        if request.method == 'POST':
            if 'create_folder' in request.POST:
                form = FolderForm(request.POST)
                if form.is_valid():
                    parent_folder_id = request.POST.get('parent_folder_id')
                    parent_folder = get_object_or_404(Folder, id=parent_folder_id, owner=request.user) if parent_folder_id else None
                    folder = form.save(commit=False)
                    folder.owner = request.user
                    folder.parent = parent_folder
                    folder.save()

                    return redirect('foldermaster:foldermanagement', folder_id=folder.parent.id if folder.parent else None)
                context['folder_form'] = form

            elif 'upload_file' in request.POST:
                form = FileForm(request.POST, request.FILES)
                if form.is_valid():
                    new_file = form.save(commit=False)
                    new_file.owner = request.user
                    new_file.folder = get_object_or_404(Folder, id=request.POST.get('parent_folder_id'), owner=request.user) if request.POST.get('parent_folder_id') else None
                    file_size = new_file.file.size
                    if storage_used + file_size > storage_limit:
                        context['error'] = "Você excedeu o limite de armazenamento de 50 MB."
                    else:
                        new_file.save()
                        storage_used += file_size
                        request.user.storage_used = storage_used
                        request.user.save()
                        return redirect('foldermaster:foldermanagement', folder_id=new_file.folder.id if new_file.folder else None)
                context['file_form'] = form

        else:
            context['folder_form'] = FolderForm()
            context['file_form'] = FileForm()

    except Exception as e:
        print(f"Erro durante o gerenciamento de pasta: {str(e)}")
        context['error'] = "Ocorreu um erro durante o processamento. Por favor, tente novamente mais tarde."

    return render(request, 'foldermaster/foldermanagement.html', context)

def get_breadcrumbs(folder):
    breadcrumbs = []
    current_folder = folder
    while current_folder:
        breadcrumbs.insert(0, (current_folder.name, current_folder.id))
        current_folder = current_folder.parent
    return breadcrumbs



@login_required
def foldermanagement_root(request, folder_id):
    try:
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
        context = {
            'folder': folder,
            'subfolders': folder.children.all(),
            'files': folder.files.all()
        }
        return render(request, 'foldermaster/foldermanagement.html', context)
    except Http404:
        return HttpResponse("A pasta não foi encontrada.", status=404)

def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response

def index(request):
    return redirect('foldermaster:foldermanagement')

def some_view(request):
    folder_id = 1 
    return redirect('foldermaster:foldermanagement', folder_id=folder_id)




@login_required
def upload_file(request, folder_id=None):
    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = form.cleaned_data['filename']
            file = request.FILES['file']
            file_model = File(name=file_name, file=file, folder=folder, owner=request.user)
            file_model.save()
            if folder_id:
                return redirect('foldermaster:foldermanagement_with_folder', folder_id=folder_id)
            else:
                return redirect('foldermaster:foldermanagement')
    else:
        form = FileUploadForm()

    return render(request, 'foldermaster/upload_file.html', {'form': form, 'folder': folder})

@login_required
def upload_folder(request, folder_id=None):
    folder = None
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    if request.method == 'POST' and request.FILES.get('zip_file'):
        zip_file = request.FILES['zip_file']
        
        # Extrair o arquivo ZIP
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall('/tmp/extracted_folder')  # Extrair para um diretório temporário
            
            # Processar a estrutura extraída
            process_extracted_folder('/tmp/extracted_folder', folder, request.user)

        if folder_id:
            return redirect('foldermaster:foldermanagement_with_folder', folder_id=folder_id)
        else:
            return redirect('foldermaster:foldermanagement')

    context = {
        'folder': folder,
    }
    return render(request, 'foldermaster/upload_folder.html', context)

def user_is_normal(user):
    return not user.is_staff

def process_extracted_folder(path, parent_folder, user):
    for root, dirs, files in os.walk(path):
        relative_root = os.path.relpath(root, path)
        current_folder = create_folders_from_path(relative_root, parent_folder, user)
        
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(file_path, path)
            
            # Save file
            file_model = File(name=file_name, folder=current_folder, owner=user)
            with open(file_path, 'rb') as f:
                file_model.file.save(file_name, ContentFile(f.read()))
            file_model.save()

def create_folders_from_path(path, parent_folder, user):
    parts = path.split(os.sep)
    current_folder = parent_folder
    for part in parts:
        if part:
            folder, created = Folder.objects.get_or_create(name=part, parent=current_folder, owner=user)
            current_folder = folder
    return current_folder

@login_required
def folder_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    subfolders = folder.children.all()
    files = folder.files.all()
    return render(request, 'foldermaster/folder_view.html', {'folder': folder, 'subfolders': subfolders, 'files': files})



@login_required
def create_folder(request, folder_id=None):
    parent_folder = None
    if folder_id:
        parent_folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            new_folder = form.save(commit=False)
            new_folder.owner = request.user
            new_folder.parent = parent_folder
            new_folder.save()
            if parent_folder:
                return redirect('foldermaster:foldermanagement_with_folder', folder_id=parent_folder.id)
            else:
                return redirect('foldermaster:foldermanagement')
    else:
        form = FolderForm()
    
    return render(request, 'foldermaster/create_folder.html', {'form': form, 'parent_folder': parent_folder})




@login_required
def delete_file(request, file_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Method Not Allowed') 

    try:
        file = File.objects.get(pk=file_id, owner=request.user)
        file.delete()

        request.user.storage_used -= file.file.size
        request.user.save()

        return JsonResponse({'success': True})
    except (File.DoesNotExist, PermissionError):
        return JsonResponse({'error': 'Arquivo não encontrado ou permissão negada'}, status=404)
    


User = get_user_model()

@login_required
def delete_folder(request, folder_id):
    try:
        folder = get_object_or_404(Folder, pk=folder_id, owner=request.user)
        print(f"Request method: {request.method}")
        print(f"Folder found: {folder.id}")

        if request.method == 'POST':
            def recursively_delete_folder(folder):
                storage_reduction = 0

                files = File.objects.filter(folder=folder)
                files_size = sum(file.file.size for file in files)
                storage_reduction += files_size

                for child_folder in folder.children.all():
                    storage_reduction += recursively_delete_folder(child_folder)

                files.delete()

                folder.delete()

                return storage_reduction

            storage_reduction = recursively_delete_folder(folder)
            print(f"Storage reduction: {storage_reduction}")

            user = request.user
            if hasattr(user, 'storage_used'):
                user.storage_used -= storage_reduction
                user.save()
            else:
                print("User does not have 'storage_used' attribute")

            parent_folder = folder.parent
            return redirect('foldermaster:foldermanagement')
        else:
            context = {
                'folder': folder
            }
            return render(request, 'foldermaster/delete_folder.html', context)

    except Folder.DoesNotExist:
        return JsonResponse({'error': 'Pasta não encontrada'}, status=404)
    except PermissionError:
        return JsonResponse({'error': 'Permissão negada'}, status=403)

