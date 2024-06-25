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
        'class' : 'form_control'
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

    email = forms.EmailField(
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
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat password',
            'class': 'form-control'
        })
    )

    account_type = forms.ChoiceField(
        choices=[('normal', 'Normal'), ('staff', 'Staff')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'account_type')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email