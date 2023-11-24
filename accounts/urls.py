from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from accounts.views import (RegisterAPIView,
                            UserInfoAPIView,
                            UserMessageSellAPIView,
                            BuyMessagesAPIView,
                            LogoutView,
                            LogoutFromAllView)

urlpatterns =[
    path('register', RegisterAPIView.as_view(), name='register'),
    path('user-info', UserInfoAPIView.as_view(), name='user-info'),
    path('user-sell', UserMessageSellAPIView.as_view(), name='user-sell'),
    path('user-buy', BuyMessagesAPIView.as_view(), name='user-buy'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout-all/', LogoutFromAllView.as_view(), name='auth_logout'),
]