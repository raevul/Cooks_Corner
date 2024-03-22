from rest_framework import serializers

from user.models import AuthorProfile
from .models import Recipe


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProfile
        fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'image']


class RecipeDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'image', 'time', 'description',
                  'author', 'difficulty', 'category', 'ingredients']

    def create(self, validated_data):
        author_profile = self.context['request'].user.author
        validated_data['author'] = author_profile
        return Recipe.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.time = validated_data.get('time', instance.time)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.ingredients = validated_data.get('ingredients', instance.ingredients)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.save()
        return instance
