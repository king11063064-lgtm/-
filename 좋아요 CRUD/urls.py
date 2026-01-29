from django.urls import path
from apps.products import views

urlpatterns = [
    # 상품 목록 및 생성: /products/
    path("", views.ProductListCreateAPIView.as_view(), name="product-create-list"),

    # 상품 상세 조회/수정/삭제: /products/<id>/
    path("<int:product_id>/", views.ProductRetrieveUpdateDestroyAPIView.as_view(), name="product-detail"),
    # feature/PostLikeAPI 전용 경로

    # [신규] 상품 좋아요 토글: /products/<id>/like/
    path("<int:product_id>/like/", views.ProductLikeAPIView.as_view(), name="product-like"),
]