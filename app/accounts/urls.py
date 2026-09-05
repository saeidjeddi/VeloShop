from django.urls import path
from .views import (
    UserLoginEmailView,
    VerifyUserEmailOTPView,
    RegisterUserView,
    VerifyRegisterUserEmailOTPView,
    ChangePasswordUserView,
    ForgetPasswordView,
    VerifyForgotPasswordResetOTPView,
    AcceptForgotPasswordResetOTPView
)
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('login/', UserLoginEmailView.as_view()),
    path('verify/login/', VerifyUserEmailOTPView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('verify/register/', VerifyRegisterUserEmailOTPView.as_view()),
    path('change_password/', ChangePasswordUserView.as_view()),
    path('forget_password/', ForgetPasswordView.as_view()),
    path('verify/forgot_password/', VerifyForgotPasswordResetOTPView.as_view()),
    path('accept/verify/forgot_password/', AcceptForgotPasswordResetOTPView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]
