from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list, name='home'), 
    path('add/', views.add_recipe, name='add_recipe'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('recipes/<int:recipe_id>/rate/', views.rate_recipe, name='rate_recipe'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('favorites/', views.favorite_recipes, name='favorite_recipes'),
    path('recipes/<int:recipe_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'), 
]
