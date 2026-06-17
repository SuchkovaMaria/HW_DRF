from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from course.models import Course, Lesson

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    """Модель платежей"""

    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Ученик", blank=True, null=True)
    created_payments = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания платежа")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Курс", blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name="Урок", blank=True, null=True)
    amount = models.FloatField(verbose_name="Сумма оплаты", help_text="Укажите сумму оплаты")
    payment_method = models.CharField(
        max_length=11, verbose_name="Способ оплаты", help_text="Укажите способ оплаты: наличные или перевод на счет"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.payment_method