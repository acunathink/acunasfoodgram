from rest_framework import serializers

from recipes.models import Ingredient, RecipeIngredients, RecipeTags, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = 'id', 'name', 'measurement_unit'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', read_only=True)
    name = serializers.CharField(
        source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = RecipeIngredients
        fields = 'id', 'name', 'amount', 'measurement_unit'


class RecipeTagSerializer(serializers.ModelSerializer):
    color = serializers.StringRelatedField(source='tag.color', read_only=True)
    name = serializers.StringRelatedField(source='tag.name')
    id = serializers.PrimaryKeyRelatedField(source='tag.id', read_only=True)
    slug = serializers.StringRelatedField(source='tag.slug')

    class Meta:
        model = RecipeTags
        fields = ('id', 'name', 'color', 'slug')


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
