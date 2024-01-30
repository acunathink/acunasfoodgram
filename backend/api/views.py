from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import IngredientSerializer, TagSerializer
from recipes.models import Ingredient, Recipe, Tag
from recipes.serializers import RecipeSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = RecipeSerializer
