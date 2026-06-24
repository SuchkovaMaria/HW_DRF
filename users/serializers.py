from rest_framework import serializers

from users.models import Payments, User


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['id', 'user', 'created_payments', 'course', 'lesson', 'amount', 'payment_method', 'link', 'session_id']
        read_only_fields = ['link', 'session_id', 'user']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password','last_login', 'phone', 'avatar', 'city', 'is_staff', 'is_active', 'date_joined']
