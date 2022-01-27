from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    create_token,
    sign_up,
)

app_name = "api"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"titles", TitleViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(r"users", UserViewSet)

auth_urls = [
    path("signup/", sign_up, name="signup"),
    path("token/", create_token, name="token"),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(auth_urls)),
]
