from celery import shared_task
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from config.settings import EMAIL_HOST_USER
from course.models import Course


@shared_task
def mail_about_update_course(emails, course_id):
    course = get_object_or_404(Course, pk=course_id)
    host = "http://127.0.0.1:8000/"
    url = f"http://{host}/course/{course_id}/"
    send_mail(
        subject="Изменения курса",
        message=f"Спешим сообщить, что курс {course.name}, на который вы подписаны обновился, скорее смотри что там нового\n{url}",
        from_email=EMAIL_HOST_USER,
        recipient_list=emails
    )
