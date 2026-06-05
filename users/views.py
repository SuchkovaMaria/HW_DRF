from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsList(generics.ListCreateAPIView):
    """Вывод списка уроков"""
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    search_fields = ('payment_method',)
    ordering_fields = ('created_payments',)