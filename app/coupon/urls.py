from django.urls import path

from .views import ApplyCouponProductAPIView


urlpatterns = [
    path('apply-coupon-product/', ApplyCouponProductAPIView.as_view()),
]