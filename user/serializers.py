from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import AuthorProfile


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProfile
        fields = '__all__'


class AddAuthorProfileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    image = serializers.ImageField()
    bio = serializers.CharField(max_length=250, write_only=True)

    def create(self, validated_data):
        return AuthorProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(min_length=8, max_length=16, write_only=True)
    confirm_password = serializers.CharField(min_length=8, max_length=16, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise ValidationError({"data": "Пароли не совпадают"})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise ValidationError({"data": "Это аккаунт уже зарегистрирован"})

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        AuthorProfile.objects.create(user=user, name=user.username, email=user.email)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8, max_length=16)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise ValidationError({"error": "Введите имя пользователя и пароль"})
        author = authenticate(username=username, password=password)
        return {"username": username, 'password': password}


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()


