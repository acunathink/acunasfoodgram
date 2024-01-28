from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = TagSerializer
    pagination_class = None


class ingredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = IngredientSerializer
    pagination_class = None
