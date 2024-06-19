from django.shortcuts import render , redirect 
from django.contrib.auth import authenticate , login , logout
from django.contrib  import messages
from foldermaster.models import Folder
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test



from .forms import SignupForm , LoginForm



def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin:index')
        else:
            folder_id = get_folder_id_for_user(request.user)
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
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                print(user.is_satff)
                return redirect(settings.ADMIN_URL)
            else:
                folder_id = get_folder_id_for_user(user)
                return redirect('foldermaster:foldermanagement', folder_id=folder_id)
        else:
            error_message = 'Invalid username or password.'
    
    context = {'form': form, 'error_message': error_message}
    return render(request, 'core/login.html', context)


@staff_member_required
def admin_view(request):
    return redirect(settings.ADMIN_URL)

def logout_view(request):
    logout(request)
    return redirect('core:index')
