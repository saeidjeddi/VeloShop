from django.urls import path

from .views import PaymentProductRequestAPIView, ZarinpalCallbackAPIView, PaymentStatusAPIView

app_name = "payment"

urlpatterns = [
    path("zarinpal/payment/", PaymentProductRequestAPIView.as_view(), name="zarinpal-payment"),
    path("zarinpal/callback/", ZarinpalCallbackAPIView.as_view(), name="zarinpal-callback"),
    path("<int:payment_id>/status/", PaymentStatusAPIView.as_view(), name="payment-status")
]
