from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from user.models import AuthorProfile
from .models import Recipe
from .permissions import IsAuthorOrReadOnly
from .serializers import RecipeSerializer, RecipeDetailSerializer, AuthorProfileSerializer


class RecipeByCategoryListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=['Recipe'],
        operation_description="Эндпоинт для фильтрации по категориям (префикс/?category=Breakfast)",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        responses={
            200: RecipeSerializer(many=True),
            401: "Неверные учетные данные",
            404: "Рецепт не найден",
            500: "Ошибка сервера"
        }
    )
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
    parser_classes = [MultiPartParser]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(
        tags=['Recipe'],
        operation_description="Эндпоинт для поиска рецепта по названию (префикс/?search=Суп)",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
        responses={
            200: RecipeSerializer(),
            401: "Неверные учетные данные",
            404: "Рецепт не найден",
            500: "Ошибка сервера"
        }
    )
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
    parser_classes = [MultiPartParser]
    filter_backend = [SearchFilter]
    search_fields = ['title']

    @swagger_auto_schema(
        tags=['Author'],
        operation_description="Эндпоинт для поиска автора по имени (префикс/?search=Ular)",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
        responses={
            200: AuthorProfileSerializer(),
            401: "Неверные учетные данные",
            404: "Рецепт не найден",
            500: "Ошибка сервера"
        }
    )
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
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=['Recipe'],
        operation_description="Эндпоинт для добавления рецепта",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER),
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'time': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'difficulty': openapi.Schema(type=openapi.TYPE_STRING),
                'ingredients': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER))
            },
            required=['title', 'category', 'image', 'time', 'description', 'difficulty', 'ingredients']
        ),
        responses={
            201: "Рецепт успешно создан",
            401: "Неверные учетные данные",
            400: "Неверный запрос",
            500: "Ошибка сервера"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RecipeDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            author = request.user
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=['Recipe'],
        operation_description="Эндпоинт для просмотра детальной страницы. Автор может изменить или удалить рецепт",
        responses={
            200: RecipeDetailSerializer(),
            401: "Неверные учетные данные",
            404: "Рецепт не найден",
            500: "Ошибка сервера"
        }
    )
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
