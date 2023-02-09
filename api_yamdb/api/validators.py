from django.core.exceptions import ValidationError


def validate_user(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Введите другое имя пользователя.'
        )
    return value
