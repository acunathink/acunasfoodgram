from django_filters import AllValuesMultipleFilter
from django_filters import rest_framework as filter

from recipes.models import Recipe


class RecipeFieldsFilter(filter.FilterSet):
    """Класс RecipeFieldsFilter используется для добавления возможности
    добавлять к запросам параметры фильтрации и поиска."""

    tags = AllValuesMultipleFilter(field_name='tags__slug')
    ingredient = AllValuesMultipleFilter(field_name='ingredients__name')
    is_favorited = filter.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filter.BooleanFilter(method='filter_is_in_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'cooking_time', 'ingredient',
                  'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, _, value):
        if not value:
            return queryset
        return queryset.filter(is_favorited=True)

    def filter_is_in_cart(self, queryset, _, value):
        if not value:
            return queryset
        return queryset.filter(is_in_shopping_cart=True)
