from django.urls import path

from .views import (RecipeByCategoryListAPIView, RecipeDetailAPIView,
                    AddRecipeAPIView, RecipeSearchAPIView, AuthorSearchAPIView)


urlpatterns = [
    path('recipes/', RecipeByCategoryListAPIView.as_view()),   # ?category=1
    path('recipes/search/', RecipeSearchAPIView.as_view()),    # ?search=test
    path('authors/', AuthorSearchAPIView.as_view()),
    path('recipes/create/', AddRecipeAPIView.as_view()),
    path('recipes/<int:recipe_id>/', RecipeDetailAPIView.as_view()),
]
