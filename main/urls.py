from django.urls import path
from .views import CreateAdvertisementDetskiymirView, GetAdvertisementDetskiymirView

urlpatterns=[
    path('detskiymir/<str:slug>',GetAdvertisementDetskiymirView.as_view(), name='get-advertisement-detskiymir'),
    path('create-detskiymir', CreateAdvertisementDetskiymirView.as_view(), name='create-advertisement-detskiymir'),


]


