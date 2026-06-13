from django.db.migrations import serializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer


class PaymentsList(generics.ListCreateAPIView):
    """Вывод списка уроков"""
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    search_fields = ('payment_method',)
    ordering_fields = ('created_payments',)


class UsersCreateView(CreateAPIView):
    """Класс создания пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        data=request.data

        user = User.objects.create(**data)
        user.set_password(data.get("password"))
        user.save()
        return Response({"email": user.email}, status=status.HTTP_201_CREATED)

class UsersRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """Класс для изменения/удаления/вывода пользлвателя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', True))
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = request.data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return Response({"email": user.email, "Изменения": "Выполнены"},status=status.HTTP_200_OK)