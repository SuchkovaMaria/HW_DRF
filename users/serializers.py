from rest_framework import serializers

from users.models import Payments


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['id', 'user', 'created_payments', 'course', 'lesson', 'amount', 'payment_method']