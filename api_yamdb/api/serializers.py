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

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    # category = CategorySerializer(many=True, read_only=True)
    # category = SlugRelatedField(slug_field='titles', read_only=True)
    # category = serializers.SlugRelatedField(slug_field='titles', queryset=Category.objects.all())
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category).data
        return rep

    class Meta:
        fields = ('id', 'name', 'year', 'category', )
        model = Title
