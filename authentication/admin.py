from django.contrib import admin
from recipes.models import Recipe, Category, Tag

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Tag)
