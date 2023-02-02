from api_yamdb.settings import LENGTH_TEXT_COMMENT, LENGTH_TEXT_REVIEW
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import LEN_FOR_NAME, CUT_TEXT
from users.models import User
from .base_models import BaseModelGenreCategory
from .validators import validate_year


class Category(BaseModelGenreCategory):

    class Meta(BaseModelGenreCategory.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(BaseModelGenreCategory):

    class Meta(BaseModelGenreCategory.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=LEN_FOR_NAME)
    year = models.PositiveSmallIntegerField(
        'Год', db_index=True, validators=[validate_year])
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='жанры')

    def __str__(self):
        return f'{self.title} {self.genre}'

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class BaseReviewCommentModel(models.Model):
    """Базовый абстрактный класс для Review и Comment."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:CUT_TEXT]


class Review(models.Model):
    """Класс отзывов."""

    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Aвтор'
    )
    score = models.PositiveIntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:LENGTH_TEXT_REVIEW]


class Comment(models.Model):
    """Класс комментариев."""

    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LENGTH_TEXT_COMMENT]
