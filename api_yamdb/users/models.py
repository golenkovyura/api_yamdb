from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import username_validator, validate_user


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
    username = models.CharField(max_length=settings.USERNAME_NAME,
                                validators=[username_validator,
                                            validate_user],
                                unique=True)

    email = models.EmailField(max_length=settings.EMAIL, unique=True)

    role = models.CharField(
        'Роль',
<<<<<<< HEAD
        max_length=settings.LEN_FOR_NAME,
=======
        max_length=settings.ROLE_TEXT,
>>>>>>> 7fed67e29e19d8b21c2f2e2eae3a03d5e2db2a1a
        choices=ROLES, default=USER
    )
    bio = models.TextField('Об авторе', null=True, blank=True)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_staff

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
