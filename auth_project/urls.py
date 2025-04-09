from django.urls import path, include
from authentication import views
from allauth.account import views as account_views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'), 
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path("reset-password/", views.password_reset_request, name="password_reset"),
    path("reset-password/done/", views.password_reset_done, name="password_reset_done"),
    path('reset-password-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), 
]
