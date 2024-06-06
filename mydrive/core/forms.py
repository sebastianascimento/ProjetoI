from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User


class ChangeForm(AuthenticationForm):
    newpassword = forms.CharField(widget=forms.PasswordInput(attrs={
         'placeholder' : 'New Password',
         'class' : 'form_control'
    }))

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs= {
            'placeholder' : 'Your Username',
            'class' : 'form_control'
            }))

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
    }))
     


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': ('Your Username'),
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your email addres',
            'class': 'form-control'
        })
    )

    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        label=("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')




    def clean_account_type(self):
        account_type = self.cleaned_data.get('account_type')
        if account_type not in ['normal', 'staff']:
            raise forms.ValidationError("Invalid account type.")
        return account_type
