from django.db.models import fields
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, GenreTitle


class CategorySerializer(serializers.ModelSerializer):
    # title = serializers.SlugRelatedField(slug_field='titles', read_only=True)
    
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
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    # category = CategorySerializer(many=True, read_only=True)
    # category = SlugRelatedField(slug_field='titles', read_only=True)
    # category = serializers.SlugRelatedField(slug_field='titles', queryset=Category.objects.all())
    
    # genre = SlugRelatedField(slug_field='genres', read_only=True)
    # genre = GenreSerializer(many=True, required=False)
    # genre = SlugRelatedField(slug_field='genres', queryset=Genre.objects.all())
    # genre = serializers.PrimaryKeyRelatedField(read_only=True)

    # genre = SlugRelatedField(slug_field='titles', read_only=True)
    # genre = serializers.SlugRelatedField(slug_field='titles', read_only=True)
    # genre = GenreTitleSerializer(many=True, required=False)

    genre = GenreTitleSerializer(many=True, required=False)

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['category'] = CategorySerializer(instance.category).data
    #     rep['genre'] = CategorySerializer(instance).data
    #     return rep

    class Meta:
        fields = ('id', 'name', 'year', 'genre', )
        model = Title



