# from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from recipes.models import Subscriber, User
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

    # def perform_create(self, serializer):
    #     author_id = self.kwargs.get('author_id')
    #     print(f'\t author_id: {author_id}')
    #     print(f'\t .validated_data: {serializer.validated_data}')
    #     author = get_object_or_404(User, pk=author_id)
    #     print(f'\t author: {author}')
    #     serializer.save(subscribe=self.request.user, author=author)
    #     print(f'serializer: {serializer}')
