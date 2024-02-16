from collections import Counter

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.serializers import ValidationError

from recipes.models import RecipeIngredients, RecipeTags


def find_duplicates(obj_list):
    return [obj for obj, count in Counter(
        obj_list).items() if count > 1]


def get_object_or_validation_error(model, pk, err_str):
    try:
        obj = model.objects.get(pk=int(pk))
    except ObjectDoesNotExist as exc:
        raise ValidationError(err_str) from exc
    return obj


def update_ingredients(recipe, ingredients):
    if ingredients is None:
        return
    recipe.ingredients.clear()
    updated_ingredients = [
        RecipeIngredients(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        ) for ingredient in ingredients
    ]
    RecipeIngredients.objects.bulk_create(updated_ingredients)


def update_tags(recipe, tags):
    if tags is None:
        return
    recipe.tags.clear()
    updated_tags = [
        RecipeTags(
            recipe=recipe,
            tag=tag,
        ) for tag in tags
    ]
    RecipeTags.objects.bulk_create(updated_tags)
