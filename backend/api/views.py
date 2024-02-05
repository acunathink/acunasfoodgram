from django.shortcuts import get_object_or_404

from django_filters import CharFilter
from django_filters import rest_framework as filter
from rest_framework import permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (IngredientRecipeSerializer, IngredientSerializer,
                             TagSerializer)
from recipes.models import Ingredient, Recipe, ShoppingCart, Tag
from recipes.serializers import (RecipeCreateSerializer, RecipeSerializer,
                                 ShoppingCartSerializer)
from users.models import User


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeFilter(filter.FilterSet):
    tags = CharFilter(field_name='tags__slug')
    ingredient = CharFilter(field_name='ingredients__name')

    class Meta:
        model = Recipe
        fields = (
            'author', 'tags', 'cooking_time', 'ingredient'
        )


class RecipeViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create',):
            return RecipeCreateSerializer

        return RecipeSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['create', 'retrieve', 'list']:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class APIRecipeCard(APIView):
    def get(self, request):
        if request._user.is_authenticated:
            user: User = request.user
            ingredients_list = Ingredient.objects.values(
                'id', 'name', 'measurement_unit', 'recipes__amount', 'recipes__recipe'
            ).filter(recipes__recipe__shoppers__user=user)
            shop_list = {}
            for ingredient in ingredients_list:
                print(ingredient)
                if ingredient['id'] not in shop_list:
                    shop_list[ingredient['id']] = ingredient
                else:
                    shop_ingredient = shop_list[ingredient['id']]
                    shop_ingredient['recipes__amount'] += ingredient['recipes__amount']
                    shop_list[ingredient['id']] = shop_ingredient

            # serializer = IngredientRecipeSerializer(
            #     data=ingredients_list, many=True)
            # if serializer.is_valid():
            return Response(shop_list, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, id):
        if request._user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
