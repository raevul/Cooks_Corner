from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import AuthorProfile


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProfile
        fields = ['id', 'username', 'email']


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
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise ValidationError({"data": "Это имя пользователя уже зарегистрирован"})

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        AuthorProfile.objects.create(user=user, username=user.username, email=user.email)
        return user


