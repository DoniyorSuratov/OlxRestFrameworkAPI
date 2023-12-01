from django.urls import path, include
from .views import (ProductPostView,
                    ProductGetView,
                    ProductUpdate,
                    UserAdverView,
                    FavouriteAdverView,
                    FavouriteGetView,
                    ProductDeleteView,
                    ProductGetVip, ProductSearchViewSet, ProductFilterView)
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('product-search', ProductSearchViewSet, basename='search_todo')

urlpatterns=[
    path('get-product',ProductGetView.as_view(), name='get-advertisement'),
    path('product', ProductPostView.as_view(), name='create-advertisement'),
    path('product-update/<int:pk>', ProductUpdate.as_view(), name='product-update'),
    path('my-advertisement', UserAdverView.as_view(), name='my-advertisement'),
    path('product-vips', ProductGetVip.as_view(), name='product-vips'),
    path('favourits/<int:pk>', FavouriteAdverView.as_view(), name='favourits-post'),
    path('favourits', FavouriteGetView.as_view(), name='favourits-get'),
    path('delete-my-advertisement/<int:pk>', ProductDeleteView.as_view(), name='delete-my-advertisement'),
    path('', include(router.urls)),
    path('product-filter-for-price', ProductFilterView.as_view(), name='product-filter-for-price'),
]


