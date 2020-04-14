from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name='password_reset_complete'),
    path('confirm-email/<key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
]
