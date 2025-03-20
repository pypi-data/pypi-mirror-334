from django.urls import path
from .views import OTPCodeSend ,Authentication

urlpatterns = [
    path('send/otpcode/', OTPCodeSend.as_view()),
    path('auth/', Authentication.as_view())
]
