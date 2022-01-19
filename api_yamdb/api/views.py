from django.core.exceptions import PermissionDenied, ValidationError, SuspiciousOperation
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, filters, pagination, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title, Comment, Review
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          CommentSerializer, ReviewSerializer, UserSerializer, SignUpSerializer, TokenRequestSerializer)
from .permissions import IsAdmin, IsAuthorizedUser
from .filters import TitleFilter
from .viewsets import CatGenViewSet


User = get_user_model()

class CategoryViewSet(CatGenViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    lookup_field = 'slug'

    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.action in ('create', 'destroy',):
            return (IsAdmin(),)
            # return (AllowAny(),)
        # elif self.action == 'GET':
        #     return (AllowAny,)
        return super().get_permissions()


    @action(detail=True, methods=['DELETE'], permission_classes=[IsAdmin()])
    def get_object(self):
        queryset = self.get_queryset()
        # queryset = self.filter_queryset(queryset)
        print('_________', queryset)

        cat = self.kwargs.get('slug')
        print('self.kwargs: ', self.kwargs)
        print('cat: ', cat)
        
        
        # for field in queryset:
        #     print(field)
        
        obj = get_object_or_404(Category, slug=cat)
        self.check_object_permissions(self.request, obj)
        print(obj)    

        return obj

    
class GenreViewSet(CatGenViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.LimitOffsetPagination
    # permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ('create', 'destroy',):
            return (IsAdmin(),)
            # return (AllowAny(),)
        # elif self.action == 'GET':
        #     return (AllowAny,)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = pagination.LimitOffsetPagination
    # permission_classes =  [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'partial_update',):
            return (IsAdmin(),)
            # return (AllowAny(),)
        # elif self.action == 'GET':
        #     return (AllowAny,)
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action == "partial_update":
            return (IsAuthorizedUser(),)
        return super().get_permissions()
    
    def get_queryset(self):
        title_id = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        queryset = Review.objects.filter(title=title_id)
        return queryset
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise SuspiciousOperation
        serializer.save(author=self.request.user, title=title)        

    def perform_destroy(self, serializer):
        if self.request.user.role == "user":
            raise PermissionDenied("У Вас нет прав на удаление")
        super().perform_destroy(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == "partial_update":
            return (IsAuthorizedUser(),)
        return super().get_permissions()
    
    def get_queryset(self):
        review_id = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        queryset = Comment.objects.filter(review=review_id)
        return queryset
        
    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
        
    def perform_destroy(self, serializer):
        if self.request.user.role == "user":
            raise PermissionDenied("У Вас нет прав на удаление")
        super().perform_destroy(serializer)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    @action(
        url_path='me',
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_current_user_info(self, request):

        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @get_current_user_info.mapping.patch
    def update_current_user_info(self, request):

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_token(request):

    username = request.data.get('username', None)
    confirmation_code = request.data.get('confirmation_code', None)

    serializer = TokenRequestSerializer(data={
        'username': username,
        'confirmation_code': confirmation_code
    })
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(
            user, confirmation_code
    ) and not confirmation_code == user.confirmation_code:
        return Response(
            'Invalid confirmation code.',
            status=status.HTTP_400_BAD_REQUEST
        )

    token = RefreshToken.for_user(user)
    response = {
        'token': str(token.access_token)
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sign_up(request):

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    send_mail(
        settings.CONFIRMATION_EMAIL_HEADER,
        confirmation_code,
        settings.CONFIRMATION_EMAIL_SENDER,
        (user.email,)
    )

    return Response(serializer.data, status=status.HTTP_200_OK)
