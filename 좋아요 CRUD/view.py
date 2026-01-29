from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, parsers
from rest_framework.response import Response

from apps.products.models import Product, Like
from apps.products.serializers import ProductSerializer, ProductDetailSerializer

class ProductListCreateAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    @extend_schema(tags=["Products"], summary="상품 목록 조회")
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')
        serializer = self.serializer_class(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["Products"], summary="상품 등록 API")
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductRetrieveUpdateDestroyAPIView(APIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]

    @extend_schema(tags=["Products"], summary="상품 상세 조회")
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = self.serializer_class(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# [핵심] feature/PostLikeAPI 전용 뷰
class ProductLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Products"], 
        summary="상품 좋아요 토글 API",
        description="id, user_id, is_liked 등 상세 정보를 반환합니다."
    )
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        # update_or_create를 사용하여 이력을 관리합니다.
        # 처음 누르면 생성(is_liked=True), 이미 있으면 상태만 토글합니다.
        like, created = Like.objects.get_or_create(user=user, product=product)

        if not created:
            like.is_liked = not like.is_liked
            like.save()

        # 팀원들이 요구한 id, user_id, product_id 필드 등을 명시적으로 반환
        return Response({
            "id": like.id,
            "user_id": user.id,
            "product_id": product.id,
            "is_liked": like.is_liked,
            "created_at": like.created_at,
            "updated_at": like.updated_at,
            "like_count": product.like_count
        }, status=status.HTTP_200_OK)
