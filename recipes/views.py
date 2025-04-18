from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Rating, Favorite, Category, Tag
from .forms import RecipeForm, RatingForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

def recipe_list(request):
    recipes = Recipe.objects.all()

    # Поиск по названию
    query = request.GET.get('q')
    if query:
        recipes = recipes.filter(title__icontains=query)

    # Фильтрация по категории
    category_filter = request.GET.get('category')
    if category_filter:
        recipes = recipes.filter(category__id=category_filter)

    # Фильтрация по тегам
    tag_filter = request.GET.get('tag')
    if tag_filter:
        recipes = recipes.filter(tags__id=tag_filter)

    # Фильтрация по автору
    author_filter = request.GET.get('author')
    if author_filter:
        recipes = recipes.filter(author__username__icontains=author_filter)

    # Фильтрация по рейтингу
    rating_filter = request.GET.get('rating')
    if rating_filter:
        # Фильтрация с использованием агрегации для среднего рейтинга
        recipes = recipes.annotate(average_rating=Avg('ratings__value')).filter(average_rating__gte=rating_filter)

    # Получаем список категорий и тегов для отображения в фильтре
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'recipes/home.html', {
        'recipes': recipes,
        'categories': categories,
        'tags': tags,
        'query': query,
        'category_filter': category_filter,
        'tag_filter': tag_filter,
        'author_filter': author_filter,
        'rating_filter': rating_filter,
    })

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

    # Проверка на наличие рецепта в избранном у текущего пользователя
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = recipe.favorite_set.filter(user=request.user).exists()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        rating_form = RatingForm(request.POST)
        
        if comment_form.is_valid() and rating_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe  
            comment.user = request.user if request.user.is_authenticated else None  # Если пользователь анонимный, оставляем поле пустым
            comment.save() 
            
            rating_value = rating_form.cleaned_data['value']
            Rating.objects.update_or_create(user=request.user, recipe=recipe, defaults={'value': rating_value})
            
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
    
    else:
        comment_form = CommentForm()
        rating_form = RatingForm()

    context = {
        'recipe': recipe,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'is_favorite': is_favorite,
        'rating_range': range(5, 0, -1),  
    }

    return render(request, 'recipes/recipe_detail.html', context)

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

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        favorite.delete()

    return redirect('recipes:recipe_detail', recipe_id=recipe.id)

@login_required
def favorite_recipes(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'recipes/favorite_recipes.html', {'favorites': favorites})
