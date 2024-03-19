from django.contrib.auth import authenticate
from rest_framework import views, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import AuthorProfile
from .serializers import (AuthorProfileSerializer, RegisterSerializer, LoginSerializer,
                          LogoutSerializer, AddAuthorProfileSerializer)


class AuthorProfileAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        try:
            author = AuthorProfile.objects.get(user=request.user)
        except AuthorProfile.DoesNotExist:
            return Response({"error": "Профиль не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorProfileSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            author = AuthorProfile.objects.get(user=request.user)
        except AuthorProfile.DoesNotExist:
            return Response({"error": "Профиль не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddAuthorProfileSerializer(instance=author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            author = AuthorProfile.objects.get(user=request.user)
        except AuthorProfile.DoesNotExist:
            return Response({"error": "Профиль не найден"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddAuthorProfileSerializer(instance=author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            token, created = Token.objects.get_or_create(user=author)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            author = authenticate(request, username=username, password=password)
            if author is not None:
                token, created = Token.objects.get_or_create(user=author)
                content = {
                    "data": "Вы успешно вошли в систему",
                    "token": token.key,
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(views.APIView):
    serializer = LogoutSerializer()

    def get(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except Exception as e:
            return Response({"error": "Произошла ошибка при выходе из системы"})
        return Response({"data": "Вы вышли из системы"})
