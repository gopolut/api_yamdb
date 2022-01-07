from django.shortcuts import render

from rest_framework import viewsets

from .serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre, Title, GenreTitle


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
