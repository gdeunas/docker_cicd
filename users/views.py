from rest_framework import generics
from users.models import User
from users.serializers import UserProfileSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Payment
from .serializers import PaymentSerializer


class UserProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Эндпоинт для просмотра и редактирования профиля пользователя.
    Принимает PUT и PATCH запросы для обновления по id.
    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ("paid_course", "paid_lesson", "payment_method")

    ordering_fields = ("payment_date",)
