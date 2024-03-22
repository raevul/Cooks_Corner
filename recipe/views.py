from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from user.models import AuthorProfile
from .models import Recipe
from .permissions import IsAuthorOrReadOnly
from .serializers import RecipeSerializer, RecipeDetailSerializer, AuthorProfileSerializer


class RecipeByCategoryListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            title_param = request.query_params.get('category', 'Breakfast')
            if title_param is not None:
                recipe = Recipe.objects.filter(category=title_param)
            else:
                recipe = Recipe.objects.all()
        except Recipe.DoesNotExist:
            return Response({"error": "Рецепты не найдены"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RecipeSerializer(recipe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeSearchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get(self, request, *args, **kwargs):
        try:
            search_query = request.query_params.get('search', '')
            recipe = Recipe.objects.filter(title__icontains=search_query)
        except Recipe.DoesNotExist:
            return Response({"error": "Рецепт не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecipeSerializer(recipe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorSearchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backend = [SearchFilter]
    search_fields = ['title']

    def get(self, request, *args, **kwargs):
        try:
            search_query = request.query_params.get('search', '')
            author = AuthorProfile.objects.filter(name__icontains=search_query)
        except AuthorProfile.DoesNotExist:
            return Response({"error": "Автор не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorProfileSerializer(author, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddRecipeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RecipeDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            author = request.user
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]

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
        serializer = RecipeDetailSerializer(instance=recipe, data=request.data, context={"request": request})
        if serializer.is_valid():
            author = request.user
            serializer.save(author=author)
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
