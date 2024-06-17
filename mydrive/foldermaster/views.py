from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from .forms import FolderForm, FileForm
from django.http import HttpResponse , Http404

@login_required
def foldermanagement(request, folder_id=None):
    context = {}

    # Se nao existir pastas cria uma pasta default
    if not Folder.objects.filter(owner=request.user).exists():
        default_folder = Folder.objects.create(name='Default Folder', owner=request.user)
        folder_id = default_folder.id

    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
        subfolders = folder.children.all()
        files = folder.files.all()
        print(f"Subfolders for folder {folder.name}: {[subfolder.name for subfolder in subfolders]}")
        context.update({
            'folder': folder,
            'subfolders': subfolders,
            'files': files,
        })
    else:
        # pastas atuais do usuario
        folders = Folder.objects.filter(owner=request.user, parent__isnull=True)
        files = File.objects.filter(owner=request.user, folder__isnull=True)
        context.update({
            'folders': folders,
            'files': files,
        })


    # Espaço usado pelo usuário
    storage_used = sum(file.file.size for file in File.objects.filter(owner=request.user))

    #Espaço disponível em 50 MB
    storage_limit = 50 * 1024 * 1024
    storage_available = storage_limit - storage_used

    #Espaço total disponível para o contexto
    context['storage_available'] = storage_available

    if request.method == 'POST':
        if 'create_folder' in request.POST:
            form = FolderForm(request.POST)
            if form.is_valid():
                parent_folder_id = request.POST.get('parent_folder_id')
                if parent_folder_id:
                    parent_folder = get_object_or_404(Folder, id=parent_folder_id, owner=request.user)
                    folder = form.save(commit=False)
                    folder.owner = request.user
                    folder.parent = parent_folder
                    folder.save()
                    return redirect('foldermaster:foldermanagement', folder_id=parent_folder.id)
                else:
                    folder = form.save(commit=False)
                    folder.owner = request.user
                    folder.save()
                    return redirect('foldermaster:foldermanagement', folder_id=folder.id)
            context['folder_form'] = form

        elif 'upload_file' in request.POST:
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                # Verificação de espaço 
                new_file = form.save(commit=False)
                new_file.owner = request.user

                #tamanho do arquivo
                file_size = new_file.file.size

                # se o espaço usado com o tamanho do novo arquivo exceder.
                if storage_used + file_size > storage_limit:
                    context['error'] = "Você excedeu o limite de armazenamento de 50 MB."
                else:
                     # salva o arquivo e atualiza o espaço usado
                    new_file.save()
                    storage_used += file_size

                    # atualiza o espaço usado
                    request.user.storage_used = storage_used
                    request.user.save()

                    return redirect('foldermaster:foldermanagement', folder_id=new_file.folder.id if new_file.folder else None)

            context['file_form'] = form
    else:
        context['folder_form'] = FolderForm()
        context['file_form'] = FileForm()

    return render(request, 'foldermaster/foldermanagement.html', context)


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
def create_folder(request):
    parent_folder_id = request.GET.get('parent_folder_id')
    parent_folder = None

    if parent_folder_id is not None:
        parent_folder = get_object_or_404(Folder, id=parent_folder_id, owner=request.user)

    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user

            if parent_folder:
                folder.parent = parent_folder
            
            folder.save()
            return redirect('foldermaster:foldermanagement', folder_id=folder.parent.id if folder.parent else None)
    else:
        form = FolderForm()

    return render(request, 'create_folder.html', {'form': form, 'parent_folder': parent_folder})
