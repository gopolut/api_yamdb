from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewset


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewset)



urlpatterns = [
    path('v1/', include(router.urls)),
]
