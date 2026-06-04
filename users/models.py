from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс Пользователь"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите email")
    phone = models.CharField(
        max_length=11, verbose_name="Телефон", blank=True, null=True, help_text="Укажите номер телефона"
    )
    avatar = models.ImageField(
        upload_to="users/avatar/", null=True, blank=True, verbose_name="Аватар", help_text="Прикрепите аватарку"
    )
    city = models.CharField(max_length=25, verbose_name="Город", blank=True, null=True, help_text="Укажите город")

    # token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
