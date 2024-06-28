from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import authenticate , login , logout , update_session_auth_hash
from django.contrib  import messages
from foldermaster.models import Folder
from django.urls import reverse, reverse_lazy
from .forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import views as auth_views


from .forms import SignupForm , LoginForm



def index(request):
    if request.user.is_authenticated:
        folder_id = get_folder_id_for_user(request.user)
        if folder_id:
            return redirect('foldermaster:foldermanagement_with_folder', folder_id=folder_id)
        else:
            return redirect('foldermaster:foldermanagement')
    else:
        return render(request, 'core/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ' Sign Up Sucess.')
            return redirect('core:login')
        else:
            print(form.errors)
            messages.error(request, 'Error in Signup. Please check the data provided.')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})

def get_folder_id_for_user(user):
    try:
        folder = Folder.objects.filter(owner=user).first() 
        if folder:
            return folder.id
        else:
            return None 
    except Folder.DoesNotExist:
        return None 
    

class CustomLoginView(auth_views.LoginView):
    template_name = 'core/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return redirect('/admin/')
        else:
            folder_id = get_folder_id_for_user(user)
            if folder_id:
                return reverse_lazy('foldermaster:foldermanagement_with_folder', kwargs={'folder_id': folder_id})
            else:
                return reverse_lazy('foldermaster:foldermanagement')
    


def login_redirect_url(request):
    user = request.user
    folder_id = get_folder_id_for_user(user)
    if folder_id is not None:
        return reverse('foldermaster:foldermanagement', kwargs={'folder_id': folder_id})
    else:
        return reverse('foldermaster:foldermanagement')


def login_view(request):
    error_message = None
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            else:
                 return redirect('foldermaster:foldermanagement')
        else:
            error_message = 'Invalid username or password.'
    
    context = {'form': form, 'error_message': error_message}
    return render(request, 'core/login.html', context)



def reset_password_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            return redirect('core:reset_password_confirm', username=username)
    else:
        form = PasswordResetForm()
    return render(request, 'core/reset_password_request.html', {'form': form})

def reset_password_confirm(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi redefinida com sucesso.')
            return redirect('core:login')
    else:
        form = SetPasswordForm(user)
    return render(request, 'core/reset_password_confirm.html', {'form': form, 'username': username})


def admin_view(request):
  return redirect('/admin/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('core:index')
