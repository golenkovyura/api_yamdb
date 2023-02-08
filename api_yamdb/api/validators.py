from django.core.exceptions import ValidationError

def validate_user(value):
        if value == 'me' or value == 'Me' or value == 'mE' or value == 'ME':
            raise ValidationError(
                'Введите другое имя пользователя.'
            )
        return value