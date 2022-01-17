from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from django.db.models import Avg
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, GenreTitle, Reviews, Comments

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    
    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Reviews
        
class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    
    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comments

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Category

    # AttributeError: 'CategorySerializer' object has no attribute 'get_queryset'
    # def to_internal_value(self, data):
    #     try:
    #         return self.get_queryset().get(**{self.slug_field: data})
    #     except (TypeError, ValueError):
    #         self.fail('invalid')

    # def to_representation(self, value):
    #     return CategorySerializer(value).data


class CategoryField(serializers.RelatedField):
    
    # def to_internal_value(self, data):
    #     try:
    #         return self.get_queryset().get(**{self.slug_field: data})
    #     except (TypeError, ValueError):
    #         self.fail('invalid')

    # def to_representation(self, value):
    #     return CategorySerializer(value).data
    
    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug
        }

    def to_internal_value(self, data):
        try:
            try:
                # slug = data['category']
                # print('-----', slug)
                # return self.get_queryset()
                print('-----', data)
                # slug = data.get('slug')

                # return self.get_queryset().get('slug')
                return Category.objects.get(slug=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Category.DoesNotExist:
            raise serializers.ValidationError(
            'Объект отсутствует'
            )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        # lookup_field = 'slug'
        model = Genre



class GenreField(serializers.SlugRelatedField):
    
    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug
        }

    def to_internal_value(self, data):
        try:
            try:
                # slug = data['category']
                # print('-----', slug)
                # return self.get_queryset()
                print('genres -----', data)
                print('g---', self.get_queryset())
                print('0000', self.get_queryset().get(**{self.slug_field: data}))

                # return self.get_queryset().get(**{self.slug_field: data})
                
                return Genre.objects.get(slug=data)
            except KeyError:
                raise serializers.ValidationError(
                    'id is a required field.'
                )
            except ValueError:
                raise serializers.ValidationError(
                    'id must be an integer.'
                )
        except Category.DoesNotExist:
            raise serializers.ValidationError(
            'Объект отсутствует'
            )


# Этот вообще не нужен
class GenreTitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = GenreTitle


class TitleSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(slug_field='titles', queryset=Category.objects.all())

    # genre = SlugRelatedField(slug_field='genres', read_only=True)
    # genre = GenreSerializer(many=True, required=False)
    # genre = SlugRelatedField(slug_field='genres', queryset=Genre.objects.all())
    # genre = serializers.PrimaryKeyRelatedField(read_only=True)

    # genre = SlugRelatedField(slug_field='titles', read_only=True)
    # genre = serializers.SlugRelatedField(slug_field='titles', read_only=True)
    # genre = GenreTitleSerializer(many=True, required=False)

    # genre = GenreTitleSerializer(many=True, required=False)

    # Работает:
    #     genre = GenreSerializer(many=True, required=False)

    # Работает:
    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['category'] = CategorySerializer(instance.category).data
    #     rep['genre'] = CategorySerializer(instance).data
    #     return rep

    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    category = CategoryField(
        # slug_field='slug',
        queryset=Category.objects.all()
    )

    # genre = serializers.SlugRelatedField(
    #     many=True,
    #     slug_field='slug',
    #     queryset=Genre.objects.all()
    # )

    # category = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Category.objects.all()
    # )
    
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        ### Пока получается не совсем-то, но стоит с чего-то начать
        title = Title.objects.get(id=obj.id)
        rating = Reviews.objects.filter(title=obj.id).aggregate(rating=Avg('score'))
        return rating

class SignUpSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):

        if value == 'me':
            raise serializers.ValidationError(
                'forbidden to use the name \'me\' as username.')
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
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )

    def update(self, obj, validated_data):

        request = self.context.get('request')
        user = request.user

        is_admin = user.role == 'admin'
        if not user.is_superuser or not is_admin:
            validated_data.pop('role', None)

        return super().update(obj, validated_data)
