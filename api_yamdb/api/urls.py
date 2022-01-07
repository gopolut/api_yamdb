from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
