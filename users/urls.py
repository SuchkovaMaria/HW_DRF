from itertools import permutations

from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import PaymentsList, UsersCreateView, UsersRetrieveUpdateDestroy

app_name = "users"

urlpatterns = [
    path("payments/", PaymentsList.as_view(), name='payments-list'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path("registr/", UsersCreateView.as_view(), name="registr"),
    path("user/<int:pk>/", UsersRetrieveUpdateDestroy.as_view(), name="retrieve-update-destroy"),
]