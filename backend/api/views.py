from django.db.models import Sum
from django.shortcuts import get_object_or_404, render

from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import AauthorOrReadOnly
from api.serializers import IngredientSerializer, TagSerializer
from api.utilities import get_object_or_validation_error
from recipes.filters import RecipeFieldsFilter
from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                            Tag)
from recipes.serializers import (FavoriteRecipeSerializer,
                                 RecipeCreateSerializer, RecipeSerializer,
                                 RecipeSubscriptionSerializer,
                                 ShoppingCartSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class FavoriteRecipeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """Класс FavoriteRecipeViewSet ограничен двумя методами:
    доступно только добавление или удаление избранных рецептов,
    id рецепта извлекается из URL."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    pagination_class = None

    @action(detail=False, methods=['delete'])
    def delete(self, request, id):
        """Сначала валидируется наличие рецепта,
        а также наличие его в списке избранных,
        затем запись удаляется."""
        recipe = get_object_or_404(Recipe, pk=id)
        delete_record = FavoriteRecipe.objects.filter(
            user=request.user, recipe=recipe).first()
        if delete_record is None:
            return Response(data={
                "error_recipe": 'Такой записи нет в избранном.'},
                status=status.HTTP_400_BAD_REQUEST)
        delete_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFieldsFilter

    def get_queryset(self):
        return Recipe.all_related_fields.with_annotate(self.request.user.pk)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'detail', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update']:
            permission_classes = [AauthorOrReadOnly]
        elif self.action in ['create', 'retrieve', 'list']:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class APIRecipeCard(APIView):
    """Класс APIRecipeCard используется для работы со списком покупок.
    Используются константы для получения ингредиентов из рецептов в корзине.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ingredients = Ingredient.objects.filter(
            recipes__recipe__shoppers__user=request.user).annotate(
            total_amount=Sum('recipes__amount')
        )
        shopping_cart = [
            {ingredient.name: (
                ingredient.total_amount,
                ingredient.measurement_unit
            )} for ingredient in ingredients
        ]
        return Response(shopping_cart, status=status.HTTP_200_OK)

    def post(self, request, id):
        recipe = get_object_or_validation_error(
            Recipe, id, 'Неверный ID рецепта.')
        request.data['user'] = request.user.id
        request.data['shop_it'] = recipe.id
        serializer = ShoppingCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe_serializer = RecipeSubscriptionSerializer(recipe)
        return Response(recipe_serializer.data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        delete_record = ShoppingCart.objects.filter(
            user=request.user, shop_it=recipe)
        if len(delete_record):
            delete_record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={
            "error_recipe": 'Такой записи в корзине нет.'},
            status=status.HTTP_400_BAD_REQUEST)


def page_not_found(request, exception):
    """Обработчик ошибки 404 - отправляет кастомный шаблон
    с соответствующим статусом.
    """
    return render(request=request, template_name='404.html',
                  status=status.HTTP_404_NOT_FOUND)
