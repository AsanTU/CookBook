from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Введите ваш email", max_length=254)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']