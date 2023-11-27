from django.urls import path
from accounts.views import (RegisterAPIView,
                            UserInfoAPIView,
                            UserMessageSellAPIView,
                            BuyMessagesAPIView,
                            LogoutView,
                            LogoutFromAllView, PasswordResetRequestView, PasswordResetConfirmView)

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('user-info', UserInfoAPIView.as_view(), name='user-info'),
    path('user-sell', UserMessageSellAPIView.as_view(), name='user-sell'),
    path('user-buy', BuyMessagesAPIView.as_view(), name='user-buy'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout-all/', LogoutFromAllView.as_view(), name='auth_logout'),
    path('reset-password', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('reset-password-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(),
         name='reset_password_confirm'),
]
