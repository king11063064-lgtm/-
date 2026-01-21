from django.urls import path
from apps.products import views

urlpatterns = [
    path("", views.ProductListCreateAPIView.as_view(), name="product-create-list"),
    path("<int:product_id>/", views.ProductRetrieveUpdateDestroyAPIView.as_view(), name="product-detail"),
    # 좋아요 CRUD를 위한 새로운 경로
    path("<int:product_id>/like/", views.ProductLikeAPIView.as_view(), name="product-like"),
]