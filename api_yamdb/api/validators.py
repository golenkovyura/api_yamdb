from django.core.exceptions import ValidationError


def validate_user(value):
    if value.title() == 'Me':
        raise ValidationError(
            'Введите другое имя пользователя.'
        )
    return value
