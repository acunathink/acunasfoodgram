from django.shortcuts import get_object_or_404

from django_filters import AllValuesMultipleFilter
from django_filters import rest_framework as filter
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import AauthorOrReadOnly
from api.serializers import IngredientSerializer, TagSerializer
from api.utilities import get_object_or_validation_error
from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                            Tag)
from recipes.serializers import (FavoriteRecipeSerializer,
                                 RecipeCreateSerializer, RecipeSerializer,
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
    http_method_names = 'post', 'delete'
    permission_classes = [permissions.IsAuthenticated]
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    pagination_class = None

    @action(detail=False, methods=['delete'])
    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        delete_record = FavoriteRecipe.objects.filter(
            user=request.user, recipe=recipe)
        delete_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeFilter(filter.FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    ingredient = AllValuesMultipleFilter(field_name='ingredients__name')

    class Meta:
        model = Recipe
        fields = (
            'author', 'tags', 'cooking_time', 'ingredient'
        )


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilter

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
    ID = 'ingredient__ingredient__id'
    NAME = 'ingredient__ingredient__name'
    MEASURE = 'ingredient__ingredient__measurement_unit'
    AMOUNT = 'ingredient__amount'

    http_method_names = ['get', 'post', 'delete']

    def get(self, request):
        if request._user.is_authenticated:
            ingredients_list = Recipe.objects.values(
                self.ID, self.NAME, self.MEASURE, self.AMOUNT).filter(
                shoppers__user=request.user
            )
            shopping_cart = self.summ_amount(ingredients_list)
            return Response(shopping_cart, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def summ_amount(self, obj_dict):
        summ_list = {}
        for obj in obj_dict:
            if obj[self.ID] not in summ_list:
                summ_list[obj[self.ID]] = obj
            else:
                summ_list[obj[self.ID]][self.AMOUNT] += obj[self.AMOUNT]

        cart = [{row[self.NAME]: (row[self.AMOUNT], row[self.MEASURE])}
                for row in summ_list.values()]
        return {'Список необходимых ингредиентов': cart}

    def post(self, request, id):
        if request._user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_validation_error(
            Recipe, id, 'Неверный ID рецепта.')
        recipe = get_object_or_404(Recipe, pk=id)
        request.data['user'] = request.user.id
        request.data['shop_it'] = recipe.id
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if request._user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, pk=id)
        delete_record = ShoppingCart.objects.filter(
            user=request.user, shop_it=recipe)
        delete_record.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
