import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers import (IngredientRecipeSerializer,
                             RecipeIngredientSerializer, RecipeTagSerializer,
                             TagSerializer)
from api.utilities import (find_duplicates, get_object_or_validation_error,
                           update_ingredients, update_tags)
from recipes.models import (FavoriteRecipe, Recipe, RecipeIngredients,
                            RecipeTags, ShoppingCart, Subscriber, Tag, User)
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
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def get_is_in_shopping_cart(self, recipe: Recipe):
        user = self.context['request'].user
        if (user.is_authenticated and ShoppingCart.objects.filter(
                shop_it=recipe, user=user).exists()):
            return True
        return False

    def get_is_favorited(self, recipe: Recipe):
        user = self.context['request'].user
        if (user.is_authenticated and FavoriteRecipe.objects.filter(
                recipe=recipe, user=user).exists()):
            return True
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientSerializer(many=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, attrs):
        check_list = 'ingredients', 'tags'
        for check in check_list:
            try:
                checked_field: list = attrs[check]
            except KeyError:
                raise serializers.ValidationError(
                    f'{check}: Это поле обязательно должно быть.')
            if len(checked_field) < 1:
                raise serializers.ValidationError(
                    f'{check}: Это поле не может быть пустым.')
            if check == 'ingredients':
                checked_field = [field['id'] for field in checked_field]
            duplicates = find_duplicates(checked_field, check)
            if len(duplicates) > 0:
                str_dups = [
                    f'{obj.name}(id:{str(obj.id)})' for obj in duplicates
                ]
                raise serializers.ValidationError(
                    f"{check}: {', '.join(str_dups)}"
                    " - дублируются в запросе."
                )
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

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.name)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        recipe.image = validated_data.get('image', recipe.image)
        update_ingredients(recipe, validated_data.get('ingredients', None))
        update_tags(recipe, validated_data.get('tags', recipe.tags))
        recipe.save()
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

    def get_is_in_shopping_cart(self, recipe: Recipe):
        return ShoppingCart.objects.filter(
            shop_it=recipe, user=self.context['request'].user).exists()

    def get_is_favorited(self, recipe: Recipe):
        return FavoriteRecipe.objects.filter(
            recipe=recipe, user=self.context['request'].user).exists()


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
    email = serializers.PrimaryKeyRelatedField(
        source='author.email', read_only=True
    )
    id = serializers.PrimaryKeyRelatedField(
        source='author', read_only=True
    )
    username = serializers.PrimaryKeyRelatedField(
        source='author.username', read_only=True
    )
    first_name = serializers.CharField(
        source='author.first_name', read_only=True
    )
    last_name = serializers.CharField(
        source='author.last_name', read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = Subscriber
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, subs_obj):
        # user = self.context['request'].user
        # if user.is_authenticated:
        #     return user.subscription.filter(author=subs_obj.author).exists()
        return True

    def get_recipes_count(self, subs_obj: Subscriber):
        return subs_obj.author.recipes.count()

    def get_recipes(self, subs_obj: Subscriber):
        recipes = subs_obj.author.recipes.all()
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit', None)
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = RecipeSubscriptionSerializer(recipes, many=True)
        return serializer.data


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

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'shop_it'),
                message="Рецепт уже в корзине."
            )
        ]


class RecipeFromKwargs:
    requires_context = True

    def __call__(self, serializer_field):
        view = serializer_field.context.get('view')
        obj = get_object_or_validation_error(
            Recipe, view.kwargs.get('id'), 'Неверный ID рецепта.')
        return obj


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects
    )
    recipe = serializers.PrimaryKeyRelatedField(
        default=RecipeFromKwargs(),
        queryset=FavoriteRecipe.objects
    )

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('user', 'recipe'),
                message="Рецепт уже в избранном."
            )
        ]
