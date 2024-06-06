from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib  import messages

from .forms import SignupForm , LoginForm


def index(request):
    if request.user.is_authenticated:
        return redirect('core:yourdrive')
    else:   
        return render(request , 'core/index.html')

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('core:yourdrive')

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


def login_view(request):
    error_message = None  
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    login(request, user)
                    return redirect('core:yourdrive')  
        else:
                error_message = 'Invalid username or password.'
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form, 'error_message': error_message})


#page users 
@login_required
def yourdrive(request):
    return render(request, 'core/yourdrive.html')

def logout_view(request):
    logout(request)
    return redirect('core:index')

