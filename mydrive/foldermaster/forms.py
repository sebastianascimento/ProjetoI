from django import forms
from .models import Folder, File
from django.db import models

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        super(FolderForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        parent_folder_id = self.data.get('parent_folder_id')
        
        if parent_folder_id:
            parent_folder = Folder.objects.get(id=parent_folder_id)
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

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(FileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        file_instance = super(FileForm, self).save(commit=False)
        if self.user:
            file_instance.owner = self.user
        if commit:
            file_instance.save()
        return file_instance

        
class FileUploadForm(forms.Form):
    filename = forms.CharField(max_length=255)
    file = forms.FileField()
    folder_id = forms.IntegerField(required=False)  

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

