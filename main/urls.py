from django.urls import path
from .views import ProductPostView, ProductGetView

urlpatterns=[
    path('product/<str:slug>',ProductGetView.as_view(), name='get-advertisement-detskiymir'),
    path('product', ProductPostView.as_view(), name='create-advertisement-detskiymir'),


]


