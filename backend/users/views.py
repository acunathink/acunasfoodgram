from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from recipes.models import Subscriber
from recipes.serializers import SubscriberSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SubscriberViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subscriber.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_class = SubscriberSerializer

    def get_queryset(self):
        return self.request.user.subscription.all()
