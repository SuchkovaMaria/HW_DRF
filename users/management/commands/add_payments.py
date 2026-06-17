from django.core.management.base import BaseCommand

from course.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):
    help = 'Добавление платежей'

    def handle(self, *args, **kwargs):

        user = User.objects.get_or_create(email="test@test1.com")[0]
        course = Course.objects.get(id=1)
        #lesson = Lesson.objects.get(id=4)
        amount = 1000.5
        payment_method = 'Наличные'
        payment = Payments.objects.create(payment_method=payment_method, amount=amount, course=course, user=user)
        self.stdout.write(self.style.SUCCESS(f'Платеж {payment.id} успешно добавлен.'))

