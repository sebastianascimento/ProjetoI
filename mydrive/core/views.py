from django.shortcuts import render , redirect 
from django.contrib.auth import authenticate , login , logout
from django.contrib  import messages
from foldermaster.models import Folder
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views


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
    

class CustomLoginView(auth_views.LoginView):
    #form_class = AuthenticationForm
    template_name = 'core/login.html'

    def get_success_url(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return redirect('/admin/')
        else:
            return reverse('foldermaster:foldermanagement')
    


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
                return redirect('/admin/')
            else:
                 return redirect(login_redirect_url(request))
        else:
            error_message = 'Invalid username or password.'
    
    context = {'form': form, 'error_message': error_message}
    return render(request, 'core/login.html', context)


def admin_view(request):
  return redirect('/admin/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:index')
