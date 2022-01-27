from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import ROLE_CHOICES


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        requires_context = True
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, obj):
        title_id = self.context["request"].parser_context["kwargs"]["title_id"]
        author = self.context["request"].user
        method = self.context["request"].method
        if (
            Review.objects.filter(
                title=title_id,
                author=author
            ).exists()
            and method != "PATCH"
        ):
            raise serializers.ValidationError(
                "Вы уже оставлял отзыв на данное произведение."
            )
        return obj


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "name",
            "slug",
        )
        lookup_field = "slug"
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "name",
            "slug",
        )
        lookup_field = "slug"
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):

    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
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
            "email",
            "username",
        )

    def validate_username(self, value):

        if value == "me":
            raise serializers.ValidationError(
                "Вы не можете использовать 'me' как username."
            )
        return value


class TokenRequestSerializer(serializers.Serializer):

    username = serializers.CharField()
    confirmation_code = serializers.CharField

    class Meta:
        require_fields = ("username", "confirmation_code")


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ['role']
        model = User


class AdminSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=ROLE_CHOICES, default="user")

    class Meta:

        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User
