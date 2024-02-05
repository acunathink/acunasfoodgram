import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers import (IngredientRecipeSerializer,
                             RecipeIngredientSerializer, RecipeTagSerializer,
                             TagSerializer)
from recipes.models import (Recipe, RecipeIngredients, RecipeTags,
                            ShoppingCart, Subscriber, Tag, User)
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(
        many=True, read_only=True, source='ingredient')
    tags = TagSerializer(
        many=True, read_only=True)
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
        exclude = ['created']

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


class AuthorFromKwargs:
    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context.get('view')
        author_id = view.kwargs.get('author_id')
        return get_object_or_404(User, pk=author_id)


class RecipeSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'


class SubscriptionsSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Subscriber
        fields = 'author',


class SubscriberSerializer(serializers.ModelSerializer):
    subscribe = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects
    )
    author = serializers.PrimaryKeyRelatedField(
        default=AuthorFromKwargs(),
        queryset=User.objects
    )

    class Meta:
        model = Subscriber
        fields = ('author', 'subscribe')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscriber.objects.all(),
                fields=('author', 'subscribe'),
                message="Повторно подписаться нельзя."
            )
        ]

    def validate(self, attrs):
        request = self.context['request']
        subscriber = attrs.get('author')
        if request.user == subscriber:
            raise serializers.ValidationError("На себя подписаться нельзя.")
        return super().validate(attrs)


class ShoppingCartSerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField(source=)

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        # fields = (
        #     'id',
        #     'shop_it__name',
        #     'shop_it__image',
        #     'shop_it__cooking_time'
        # )
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'shop_it'),
                message="Рецепт уже в корзине."
            )
        ]
