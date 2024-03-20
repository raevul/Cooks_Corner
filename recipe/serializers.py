from rest_framework import serializers

from user.serializers import AuthorProfileSerializer
from .models import Category, Recipe, Ingredient


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title', 'unit']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'author']


class RecipeDetailSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # ingredient = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'image', 'time', 'description',
                  'author', 'difficulty', 'category', 'ingredient']

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['author'] = request.user
    #
    #     category = validated_data.pop("category")
    #     ingredients_data = validated_data.pop("ingredient")
    #
    #     recipe = Recipe.objects.create(category=category, **validated_data)
    #
    #     for ingredient_data in ingredients_data:
    #         ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
    #         recipe.ingredients.add(ingredient)
    #     return recipe
