from rest_framework import serializers

from recipes.models import Ingredient, RecipeIngredients, RecipeTags, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = 'id', 'name', 'amount', 'measurement_unit'

    def get_amount(self, ingredient):
        recipe_ingredient = RecipeIngredients.objects.get(
            recipe=self.parent.root.instance, ingredient=ingredient
        )
        return recipe_ingredient.amount


class RecipeTagSerializer(serializers.ModelSerializer):
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
