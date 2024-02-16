from django_filters import AllValuesMultipleFilter
from django_filters import rest_framework as filter

from recipes.models import Recipe


class RecipeFieldsFilter(filter.FilterSet):
    """Класс RecipeFieldsFilter используется для добавления возможности
    добавлять к запросам параметры фильтрации и поиска."""

    tags = AllValuesMultipleFilter(field_name='tags__slug')
    ingredient = AllValuesMultipleFilter(field_name='ingredients__name')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'cooking_time', 'ingredient')

    def filter_queryset(self, queryset):
        if self.request.user.is_anonymous:
            return super().filter_queryset(queryset)
        if self.request.query_params.get('is_favorited', '0') == '1':
            queryset = queryset.filter(favored__user=self.request.user)
        if self.request.query_params.get('is_in_shopping_cart', '0') == '1':
            queryset = queryset.filter(shoppers__user=self.request.user)
        return super().filter_queryset(queryset)
