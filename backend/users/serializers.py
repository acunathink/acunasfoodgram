from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
User = get_user_model()

class CustomUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'password', 'first_name', 'last_name', 'username'
        )
