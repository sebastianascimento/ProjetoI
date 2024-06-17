from django import forms
from .models import Folder, File

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Recebe o usuário como argumento
        super(FolderForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        parent_folder_id = self.data.get('parent_folder_id')
        
        if parent_folder_id:
            parent_folder = Folder.objects.get(id=parent_folder_id)
            # Garante que o novo folder pertence ao mesmo owner do parent_folder
            if parent_folder.owner != self.user:
                raise forms.ValidationError("Você não tem permissão para criar uma pasta aqui.")
        
        return name

    def save(self, commit=True):
        folder = super(FolderForm, self).save(commit=False)
        folder.owner = self.user
        if commit:
            folder.save()
        return folder
class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'folder', 'file']
