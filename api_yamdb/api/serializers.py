from django.db.models import fields
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, GenreTitle, Reviews, Comments


class CategorySerializer(serializers.ModelSerializer):
    # title = serializers.SlugRelatedField(slug_field='titles', read_only=True)
    
    class Meta:
        fields = ('id', 'name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    # title_id = serializers.PrimaryKeyRelatedField(read_only=True)

    # def to_internal_value(self, data):
    #     try:
    #         return self.get_queryset().get(**{self.slug_field: data})
    #     except (TypeError, ValueError):
    #         self.fail('invalid')
    # def to_representation(self, value):
    #     return GenreSerializer(value).data

    class Meta:
        fields = '__all__'
        # lookup_field = 'slug'
        model = Genre

class GenreTitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = GenreTitle


class TitleSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    # category = CategorySerializer(many=True, read_only=True)
    # category = SlugRelatedField(slug_field='titles', read_only=True)
    # category = serializers.SlugRelatedField(slug_field='titles', queryset=Category.objects.all())
    
    # genre = SlugRelatedField(slug_field='genres', read_only=True)
    # genre = SlugRelatedField(slug_field='genres', queryset=Genre.objects.all())
    # genre = serializers.PrimaryKeyRelatedField(read_only=True)

    # genre = SlugRelatedField(slug_field='titles', read_only=True)
    # genre = serializers.SlugRelatedField(slug_field='titles', read_only=True)
    # genre = GenreTitleSerializer(many=True, required=False)
    # genre = GenreTitleSerializer(many=True, required=False)
    
    # Работает:
    #     genre = GenreSerializer(many=True, required=False)

    # Работает:
    #     def to_representation(self, instance):
    #         rep = super().to_representation(instance)
    #         rep['category'] = CategorySerializer(instance.category).data
    #         return rep

    genre = SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    
    class Meta:
        fields = "__all__"
        model = Reviews


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        fields = "__all__"
        model = Comments
