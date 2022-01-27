from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from django.db.models import Avg
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import ADMIN_ROLE


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        requires_context = True
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        model = Review

    def validate(self, obj):
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        author = self.context['request'].user
        method = self.context['request'].method
        if (
            Review.objects.filter(
                title=title_id,
                author=author
            ).exists()
            and method != 'PATCH'
        ):
            raise serializers.ValidationError(
                'Вы уже оставлял отзыв на данное произведение.'
            )
        return obj


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'
        model = Category


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return {'name': obj.name, 'slug': obj.slug}

    def to_internal_value(self, data):
        try:
            return Category.objects.get(slug=data)
        except KeyError:
            raise serializers.ValidationError('Необходимо указать slug')
        except ValueError:
            raise serializers.ValidationError(
                'Используйте формат string для slug.'
            )
        except Category.DoesNotExist:
            raise serializers.ValidationError('Объект отсутствует')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug',
        )
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return {'name': obj.name, 'slug': obj.slug}

    def to_internal_value(self, data):
        try:
            return Genre.objects.get(slug=data)
        except KeyError:
            raise serializers.ValidationError('Требуется указать slug.')
        except ValueError:
            raise serializers.ValidationError(
                'Используйте формат string для slug.'
            )
        except Category.DoesNotExist:
            raise serializers.ValidationError('Объект отсутствует')


class TitleReadSerializer(serializers.ModelSerializer):

    genre = GenreField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = CategorySerializer(required=False)
   
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title

    def get_rating(self, obj):
        scores = Review.objects.filter(title=obj.id)
        rating = scores.aggregate(rating=Avg('score'))['rating']
        return rating


class TitleWriteSerializer(serializers.ModelSerializer):

    genre = GenreField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )

    category = SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    
    class Meta:
        fields = (
            'id',
            'name',
            'year',
            # 'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class SignUpSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )

    def validate_username(self, value):

        if value == 'me':
            raise serializers.ValidationError(
                'Вы не можете использовать "me" как username.'
            )
        return value


class TokenRequestSerializer(serializers.Serializer):

    username = serializers.CharField()
    confirmation_code = serializers.CharField

    class Meta:
        require_fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def update(self, obj, validated_data):

        request = self.context.get('request')
        user = request.user

        is_admin = user.role == ADMIN_ROLE
        if not user.is_superuser or not is_admin:
            validated_data.pop('role', None)

        return super().update(obj, validated_data)
