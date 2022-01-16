from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, filters, pagination, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from reviews.models import Category, Genre, Title, Comments, Reviews
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          CommentSerializer, ReviewSerializer, UserSerializer, SignUpSerializer, TokenRequestSerializer)
from .permissions import IsAdmin

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category', 'genre', 'name', 'year',)
    
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        title_id = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        queryset = Reviews.objects.filter(title=title_id)
        return queryset
    
    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)
 
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        review_id = get_object_or_404(Reviews, id=self.kwargs.get("review_id"))
        queryset = Comments.objects.filter(review=review_id)
        return queryset
        
    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

User = get_user_model()

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
