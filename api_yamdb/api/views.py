from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .pagination import CustomPagination
from reviews.models import Category, Genre, Title, GenreTitle


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = CustomPagination

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # pagination_class = CustomPagination
