from django.db import models


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(max_length=100, verbose_name="Курс", help_text="Введите название курса")
    description = models.TextField(verbose_name="Описание", blank=True, null=True, help_text="Введите описание курса")

    # путь для сохранения превью курса
    image = models.ImageField(
        upload_to="data/image_course",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Загрузите превью курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(max_length=100, verbose_name="Урок", help_text="Введите название урока")
    description = models.TextField(verbose_name="Описание", blank=True, null=True, help_text="Введите описание урока")

    image = models.ImageField(
        upload_to="data/image_lesson",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Введите название курса",
        related_name="courses",
    )
    video_path = models.CharField(max_length=255, verbose_name="Cсылка на видео", help_text="Укажите ссылку на видео")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name
