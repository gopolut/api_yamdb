from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import Category, Genre, Title, GenreTitle


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    # def perform_create(self, serializer):
    #     # return super().perform_create(serializer)
    #     # cat = get_object_or_404(Category, pk=self.kwargs.get('category'))
    #     # cat = Category.objects.filter(slug=self.kwargs.get('titles'))
    #     print('serializer: ', serializer.data)
        
    #     serializer.save(category=4)
