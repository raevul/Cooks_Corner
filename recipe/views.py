from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from .models import Recipe, Category
from .serializers import RecipeSerializer, CategorySerializer, RecipeDetailSerializer


class RecipeListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.all()
        except Exception as e:
            return Response({"error": "Ничего не найдено"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RecipeSerializer(recipe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs['recipe_id'])
        except Recipe.DoesNotExist:
            return Response({"error", "Рецепт не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs['recipe_id'])
        except Recipe.DoesNotExist:
            return Response({"error", "Рецепт не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecipeDetailSerializer(instance=recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            recipe = Recipe.objects.get(id=kwargs['recipe_id'])
        except Recipe.DoesNotExist:
            return Response({"error", "Рецепт не найден"}, status=status.HTTP_404_NOT_FOUND)
        recipe.delete()
        return Response({"data": "Рецепт успешно удален"}, status=status.HTTP_200_OK)
