from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, PasswordResetForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile 

def home(request):
    return render(request, 'recipes/home.html')

def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('register')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home') 
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home') 
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        users = User.objects.filter(email=email)
        if users.exists():
            for user in users:
                subject = "Сброс пароля"
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                domain = request.get_host()  
                reset_url = f"http://{domain}/auth/reset-password-confirm/{uid}/{token}/"

                message = render_to_string("password_reset_email.html", {
                    "user": user,
                    "reset_url": reset_url,
                })

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

            messages.success(request, "Инструкции по сбросу пароля отправлены на вашу почту.")
            return redirect("login")
        else:
            messages.error(request, "Пользователь с таким email не найден.")

    return render(request, "password_reset.html")

def password_reset_done(request):
    return render(request, "password_reset_done.html")

def password_reset_confirm(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Пароль успешно изменён!")
                return redirect("login")
        else:
            form = SetPasswordForm(user)
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        messages.error(request, "Ссылка сброса недействительна.")
        return redirect("password_reset")

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    user = request.user

    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'authentication/edit_profile.html', {'profile_form': profile_form})