from django.contrib import admin
from django.urls import path, include
from authentication import views
from recipes import views as recipe_views 
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('authentication.urls')),
    path('recipes/', include('recipes.urls')),
    path('accounts/', include('allauth.urls')),
    path('', recipe_views.recipe_list, name='home'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)