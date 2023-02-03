from api_yamdb.settings import LIST_PER_PAGE
from django.contrib import admin

from reviews.models import Comment, Review, User


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывов."""

    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    empty_value_display = 'Значение отсутствует'
    list_filter = ('author', 'score', 'pub_date')
    list_per_page = LIST_PER_PAGE
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review'
    )
    empty_value_display = 'Значение отсутствует'
    list_filter = ('author', 'pub_date')
    list_per_page = LIST_PER_PAGE
    search_fields = ('author',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'username', 'email',
                    'bio', 'first_name', 'last_name',)