from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import Subscriber, User
from recipes.serializers import SubscriberSerializer, SubscriptionsSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action == "me":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


class SubscriberViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subscriber.objects.all()
    http_method_names = 'post', 'delete'
    serializer_class = SubscriberSerializer

    def get_queryset(self):
        return self.request.user.subscription.all()

    @action(detail=False, methods=['delete'])
    def delete(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)
        delete_record = Subscriber.objects.filter(
            subscribe=request.user, author=author)
        if len(delete_record):
            delete_record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={
            "error_id": 'Такой подписки не существует'},
            status=status.HTTP_400_BAD_REQUEST)


class SubscriptionsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = 'get',
    serializer_class = SubscriptionsSerializer
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.request.user.subscription.all()
