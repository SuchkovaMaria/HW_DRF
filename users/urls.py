from django.urls import path

from users.views import PaymentsList

app_name = "users"

urlpatterns = [
    path("payments/", PaymentsList.as_view(), name='payments-list'),
]