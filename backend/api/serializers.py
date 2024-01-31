from rest_framework import serializers

from recipes.models import (Ingredient, Recipe, RecipeIngredients, RecipeTags,
                            Tag)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeTagSerializer(serializers.ModelSerializer):
    # slug = serializers.SlugRelatedField(
    #     slug_field='tag.slug', queryset=Tag.objects.all()
    # )
    color = serializers.StringRelatedField(source='tag.color', read_only=True)
    name = serializers.StringRelatedField(source='tag.name')
    id = serializers.PrimaryKeyRelatedField(source='tag.id', read_only=True)

    class Meta:
        model = RecipeTags
        fields = ('id', 'name', 'color')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount', 'name', 'measurement_unit')
