from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters, pagination, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, Review
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    CommentSerializer,
    ReviewSerializer,
    UserSerializer,
    SignUpSerializer,
    TokenRequestSerializer,
    TitleWriteSerializer,
    AdminSerializer,
)
from .permissions import (
    IsSuperAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrModerator,
    IsMe,
)
from .filters import TitleFilter
from .viewsets import CategoryGenreViewSet


User = get_user_model()


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by("id")
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModerator,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        queryset = title.reviews.order_by("id")
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModerator,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        queryset = review.comments.order_by("id")
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsSuperAdmin,)
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ("username",)
    lookup_field = "username"

    def get_serializer_class(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.is_admin
        ):
            return AdminSerializer
        return UserSerializer

    @action(
        url_path="me",
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsMe,)
    )
    def get_current_user_info(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "PATCH":
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def create_token(request):

    username = request.data.get("username", None)
    confirmation_code = request.data.get("confirmation_code", None)

    serializer = TokenRequestSerializer(
        data={"username": username, "confirmation_code": confirmation_code}
    )
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=username)

    if (
        not default_token_generator.check_token(user, confirmation_code)
        and not confirmation_code == user.confirmation_code
    ):
        return Response(
            "Invalid confirmation code.", status=status.HTTP_400_BAD_REQUEST
        )

    token = RefreshToken.for_user(user)
    response = {"token": str(token.access_token)}
    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def sign_up(request):

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        settings.CONFIRMATION_EMAIL_HEADER,
        confirmation_code,
        settings.CONFIRMATION_EMAIL_SENDER,
        (user.email,),
    )

    return Response(serializer.data, status=status.HTTP_200_OK)
