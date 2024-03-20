from django.contrib import admin
from .models import Category, Recipe, Ingredient

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Recipe)
