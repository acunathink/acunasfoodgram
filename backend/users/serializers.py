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


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, check_user):
        user = self.context['request'].user
        if user.is_authenticated:
            return user.subscription.filter(author=check_user).exists()
        return False
