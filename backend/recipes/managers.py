from django.db import models
from django.db.models.expressions import Exists, OuterRef
from django.db.models.query import QuerySet


class RelatedFieldsManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related(
            'author', 'ingredients', 'tags',
            'shoppers', 'favored'
        )

    def with_annotate(self, user_pk):
        """Добавляет поля "is_in_shopping_cart" и "is_favorited".
        Для анонимного пользователя эти поля всегда содержат False
        """
        return self.annotate(
            is_favorited=Exists(self.filter(
                favored__user=user_pk, favored__recipe=OuterRef('pk'))),
            is_in_shopping_cart=Exists(self.filter(
                shoppers__user=user_pk, shoppers__shop_it=OuterRef('pk')))
        )
