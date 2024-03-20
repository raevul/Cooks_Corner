from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from .models import Recipe, Category, Ingredient
from .serializers import RecipeSerializer, CategorySerializer, RecipeDetailSerializer, IngredientSerializer


class CategoryAPi(APIView):
    def get(self, request):
        cat = Category.objects.all()
        serializer = CategorySerializer(cat, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeByCategoryListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            title_param = request.query_params.get('category', 'Breakfast')
            if title_param is not None:
                recipe = Recipe.objects.filter(category=title_param)
            else:
                recipe = Recipe.objects.all()
        except Exception as e:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RecipeSerializer(recipe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeSearchAPIView(APIView):
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get(self, request, *args, **kwargs):
        try:
            search_query = request.query_params.get('search', '')
            recipe = Recipe.objects.filter(title__icontains=search_query)
        except Exception as e:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RecipeSerializer(recipe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# ToDo добавить несколько ингредиентов
class AddRecipeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id
        serializer = RecipeDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def post(self, request, *args, **kwargs):
    #     # Получаем данные из запроса
    #     data = request.data
    #
    #     # Создаем сериализаторы для рецепта, категории и ингредиентов
    #     recipe_serializer = RecipeDetailSerializer(data=data)
    #     category_serializer = CategorySerializer(data=data.get('category'))
    #     ingredient_serializers = [IngredientSerializer(data=ingredient_data) for ingredient_data in
    #                               data.get('ingredients', [])]
    #
    #     # Проверяем валидность всех сериализаторов
    #     if not all([recipe_serializer.is_valid(), category_serializer.is_valid()] + [serializer.is_valid() for
    #                                                                                  serializer in
    #                                                                                  ingredient_serializers]):
    #         errors = {
    #             'recipe': recipe_serializer.errors,
    #             'category': category_serializer.errors,
    #             'ingredients': [serializer.errors for serializer in ingredient_serializers]
    #         }
    #         return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # Сохраняем категорию
    #     category = category_serializer.save()
    #
    #     # Сохраняем рецепт
    #     recipe_data = recipe_serializer.validated_data
    #     recipe = Recipe.objects.create(
    #         title=recipe_data['title'],
    #         image=recipe_data['image'],
    #         description=recipe_data['description'],
    #         time=recipe_data['time'],
    #         category=category,
    #         author=request.user,  # Устанавливаем текущего пользователя как автора рецепта
    #         difficulty=recipe_data['difficulty']
    #     )
    #
    #     # Сохраняем ингредиенты и их связи с рецептом
    #     for ingredient_serializer in ingredient_serializers:
    #         ingredient = ingredient_serializer.save()
    #         recipe.ingredients.add(ingredient)
    #
    #     # Возвращаем успешный ответ
    #     return Response(RecipeDetailSerializer(recipe).data, status=status.HTTP_201_CREATED)


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
