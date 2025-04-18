from django import forms
from .models import Recipe, Tag, Category

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
