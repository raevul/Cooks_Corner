from django.urls import path

from .views import (RecipeByCategoryListAPIView, RecipeDetailAPIView, CategoryAPi,
                    AddRecipeAPIView, RecipeSearchAPIView)


urlpatterns = [
    path('recipes/', RecipeByCategoryListAPIView.as_view()),
    path('recipes/search/', RecipeSearchAPIView.as_view()),
    path('recipes/create/', AddRecipeAPIView.as_view()),
    path('recipes/<int:recipe_id>/', RecipeDetailAPIView.as_view()),
]
