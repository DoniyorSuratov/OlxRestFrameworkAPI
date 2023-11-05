from django.urls import path
from accounts.views import (RegisterAPIView,
                            UserInfoAPIView,
                            UserMessageSellAPIView,
                            BuyMessagesAPIView)

urlpatterns =[
    path('register', RegisterAPIView.as_view(), name='register'),
    path('user-info', UserInfoAPIView.as_view(), name='user-info'),
    path('user-sell', UserMessageSellAPIView.as_view(), name='user-sell'),
    path('user-buy', BuyMessagesAPIView.as_view(), name='user-buy')
]