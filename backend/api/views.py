from django_filters import CharFilter
from django_filters import rest_framework as filter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import IngredientSerializer, TagSerializer
from recipes.models import Ingredient, Recipe, Tag, RecipeTags
from recipes.serializers import RecipeCreateSerializer, RecipeSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination


class RecipeFilter(filter.FilterSet):
    tags__slug = CharFilter(lookup_expr='tags', field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags__slug')


class RecipeViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create',):
            return RecipeCreateSerializer

        return RecipeSerializer
