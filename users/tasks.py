from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def user_deactivation():
    today = timezone.now()
    date_border = today - timezone.timedelta(days=30)
    users_date_border = User.objects.filter(last_login__lt=date_border, is_active=True, is_superuser = False)
    print(users_date_border)
    users_date_border.update(is_active=False)
