from rest_framework import serializers
from .models import CustomUser


# Сериализатор пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone_number', 'balance', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


# Сериализатор для регистрации
class RegisterSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            balance=validated_data.get('balance', 0.00)
        )
        return user
