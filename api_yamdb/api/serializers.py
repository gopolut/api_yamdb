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
        fields = ('id', 'name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    title_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Genre

class GenreTitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = GenreTitle


class TitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    
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
