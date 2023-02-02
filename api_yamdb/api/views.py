from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from reviews.models import Review, Title
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import (IsSuperUserIsAdminIsModeratorIsAuthor,
                          IsAdminOrReadOnly, IsAdmin)
from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Category, Genre, Review, Title
from users.models import User
from .mixins import ListCreateDestroyGenericViewSet


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminIsModeratorIsAuthor
    )

    def get_title(self):
        """Возвращает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения,
        где автором является текущий пользователь."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserIsAdminIsModeratorIsAuthor
    )

    def get_review(self):
        """Возвращает объект текущего отзыва."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для текущего отзыва,
        где автором является текущий пользователь."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class CategoryViewSet(ListCreateDestroyGenericViewSet):
    """Вьюсет для модели Category"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(ListCreateDestroyGenericViewSet):
    """Вьюсет для модели Genre"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title"""

    ACTIONS = ['create', 'partial_update']
    serializer_class = TitlePostSerializer
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]
    ordering_field = ('name',)

    def get_serializer_class(self):
        if self.action in self.ACTIONS:
            return TitlePostSerializer
        return TitleSerializer


