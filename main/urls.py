from django.urls import path
from .views import ProductPostView, ProductGetView, ProductUpdate

urlpatterns=[
    path('product/<str:slug>',ProductGetView.as_view(), name='get-advertisement-detskiymir'),
    path('product', ProductPostView.as_view(), name='create-advertisement-detskiymir'),
    path('product-update/<int:pk>', ProductUpdate.as_view(), name='product-update')


]


