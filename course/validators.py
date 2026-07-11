from rest_framework.serializers import ValidationError

expression_test = "https://youtube.com"


def validete_expression_test(value):
    """Проверка ссылки на ютуб"""

    if expression_test not in value:
        raise ValidationError("Неверная ссылка (допускается использовать только Youtube)")
