import base64

from django.core.files.base import ContentFile

from rest_framework import serializers

from api.serializers import (IngredientSerializer, RecipeIngredientSerializer,
                             RecipeTagSerializer, TagSerializer)
from recipes.models import Recipe, Tag
from users.serializers import CustomUserSerializer
from .models import RecipeIngredients, RecipeTags


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = ('author',)

    def validate(self, attrs):
        print(f'attrs {attrs}')
        return super().validate(attrs)


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate(self, attrs):
        ingredients = attrs['ingredients']
        if len(ingredients) < 1:
            raise serializers.ValidationError(
                'ingredients: Это поле не может быть пустым.')
        return super().validate(attrs)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        create_ingredients = [
            RecipeIngredients(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        create_tags = [
            RecipeTags(tag=tag, recipe=recipe) for tag in tags
        ]
        RecipeTags.objects.bulk_create(create_tags)
        RecipeIngredients.objects.bulk_create(create_ingredients)
        return recipe

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields.pop('tags')
        representation = super().to_representation(instance)
        representation['ingredients'] = RecipeIngredientSerializer(
            RecipeIngredients.objects.filter(recipe=instance).all(), many=True
        ).data
        representation['tags'] = RecipeTagSerializer(
            RecipeTags.objects.filter(recipe=instance).all(), many=True
        ).data
        return representation
