
from django.urls import path
from apps.products import views

urlpatterns = [
    # /products/
    path("", views.ProductListCreateAPIView.as_view(), name="product-create-list"),
    # /products/1/
    path("<int:product_id>/", views.ProductRetrieveUpdateDestroyAPIView.as_view(), name="product-detail"),
    # feature/PostLikeAPI 전용 경로
    # /products/1/like/
    path("<int:product_id>/like/", views.ProductLikeAPIView.as_view(), name="product-like"),
]