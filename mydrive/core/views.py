from django.shortcuts import render , redirect 
from django.contrib.auth import authenticate , login , logout
from django.contrib  import messages
from foldermaster.models import Folder
from django.urls import reverse
from django.contrib.auth.views import LoginView


from .forms import SignupForm , LoginForm


def index(request):
    if request.user.is_authenticated:
        folder_id = 1
        return redirect('foldermaster:foldermanagement' , folder_id=folder_id)
    else:
        return render(request, 'core/index.html')

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ' Sign Up Sucess.')
            return redirect('core:login')
        else:
            messages.error(request, 'Error in Signup. Please check the data provided.')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})

def get_folder_id_for_user(user):
    try:
        folder = Folder.objects.filter(user=user).first() 
        if folder:
            return folder.id
        else:
            return None 
    except Folder.DoesNotExist:
        return None 
    


def login_redirect_url(request):
    user = request.user
    folder_id = get_folder_id_for_user(user)
    if folder_id is not None:
        return reverse('foldermaster:foldermanagement', kwargs={'folder_id': folder_id})
    else:
        return reverse('foldermaster:foldermanagement')


def login_view(request):
    error_message = None  
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    folder_id = get_folder_id_for_user(user)
                    return redirect('foldermaster:foldermanagement' , folder_id=folder_id)
            else:
                error_message = 'Invalid username or password.'
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('core:index')
