from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'id', 'password', 'first_name', 'last_name', 'username'
        )

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     print('     --  attrs:', attrs)
    #     print('-- self.fields:', self.fields)
    #     for field in attrs:
    #         print(fields)
    #     if email is None or email == '':
    #         raise serializers.ValidationError(
    #             {"email": "Введите адрес электронной почты."}
    #         )
    #     return super().validate(attrs)


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
        )
