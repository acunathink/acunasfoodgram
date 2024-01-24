from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'password', 'first_name', 'last_name', 'username'
        )


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
        )
