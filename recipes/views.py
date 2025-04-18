from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe 
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/home.html', {'recipes': recipes})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m() 
            return redirect('recipes:home')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.author != request.user:
        return redirect('recipes:home')  

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes:home')
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {'form': form})

def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if recipe.author != request.user:
        return redirect('recipes:home')  

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipes:home') 

    return render(request, 'recipes/delete_recipe.html', {'recipe': recipe})