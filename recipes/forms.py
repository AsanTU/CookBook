from django import forms
from .models import Recipe, Tag, Category, Rating, Comment

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'photo', 'ingredients', 'instructions', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
        }

        category = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            empty_label="Выберите категорию",
            widget=forms.Select(attrs={'class': 'form-control'})
        )

        tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple,  
            required=False
        )

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {
            'value': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)])
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']