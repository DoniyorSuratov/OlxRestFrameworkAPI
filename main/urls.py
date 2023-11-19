from django.urls import path
from .views import (ProductPostView,
                    ProductGetView,
                    ProductUpdate,
                    UserAdverView,
                    FavouriteAdverView,
                    FavouriteGetView,
                    ProductDeleteView,
                    CategoryParentsView,
)

urlpatterns=[
    path('get-product',ProductGetView.as_view(), name='get-advertisement'),
    path('product', ProductPostView.as_view(), name='create-advertisement'),
    path('product-update/<int:pk>', ProductUpdate.as_view(), name='product-update'),
    path('my-advertisement', UserAdverView.as_view(), name='my-advertisement'),
    path('favourits/<int:pk>', FavouriteAdverView.as_view(), name='favourits-post'),
    path('favourits/', FavouriteGetView.as_view(), name='favourits-get'),
    path('delete-my-advertisement/<int:pk>', ProductDeleteView.as_view(), name='delete-my-advertisement'),
    path('category-parents/', CategoryParentsView.as_view(), name='category-parents'),
]

