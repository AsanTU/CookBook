from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Rating
from .forms import RecipeForm, RatingForm, CommentForm
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

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        rating_form = RatingForm(request.POST)
        
        if comment_form.is_valid() and rating_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe  
            comment.user = request.user  
            comment.save() 
            
            rating_value = rating_form.cleaned_data['value']
            Rating.objects.update_or_create(user=request.user, recipe=recipe, defaults={'value': rating_value})
            
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
    
    else:
        comment_form = CommentForm()
        rating_form = RatingForm()

    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'comment_form': comment_form, 'rating_form': rating_form})

def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            Rating.objects.update_or_create(user=request.user, recipe=recipe, defaults={'value': value})
            return redirect('recipes:home')
    else:
        form = RatingForm()

    return render(request, 'recipes/rate_recipe.html', {'form': form, 'recipe': recipe})
