from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User


class ChangeForm(AuthenticationForm):
    newpassword = forms.CharField(widget=forms.PasswordInput(attrs={
         'placeholder' : 'New Password',
         'class' : 'form-control'
    }))

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs= {
            'placeholder' : 'Your Username',
            'class' : 'form-control'
            }))

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class' : 'form-control'
    }))
     
class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Username',
            'class': 'form-control'
        })
    )

    email= forms.EmailField(
        max_length=250,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email address',
            'class': 'form-control'
        })
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
            'class': 'form-control'
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].strip = True 

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
