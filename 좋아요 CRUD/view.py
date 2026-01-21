from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, parsers
from rest_framework.response import Response
from apps.products.models import Product
from apps.products.serializers import ProductSerializer, ProductDetailSerializer

class ProductListCreateAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]
    
    @extend_schema(tags=["Products"], summary="상품 등록 API")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 실제 저장 로직: serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    @extend_schema(operation_id="v1_products_list", tags=["Products"], summary="상품 목록 조회", responses={200: ProductSerializer(many=True)})
    def get(self, request):
        mock_data = [Product(id=i, name=f"Mock {i}", price=i*1000, image="m.jpg") for i in range(1, 6)]
        serializer = self.serializer_class(mock_data, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductRetrieveUpdateDestroyAPIView(APIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser]
    
    @extend_schema(tags=["Products"], summary="상품 상세 조회")
    def get(self, request, product_id):
        mock_data = Product(id=product_id, name="Mock Detail", description="Desc", price=10000, image="m.jpg")
        serializer = self.serializer_class(mock_data, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # ... put, delete 로직 유지 ...

class ProductLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Products"], summary="상품 좋아요 토글 API", description="좋아요 등록/취소를 수행합니다.")
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        if product.like_users.filter(id=user.id).exists():
            product.like_users.remove(user)
            return Response({"status": "unliked", "like_count": product.like_count}, status=status.HTTP_200_OK)
        else:
            product.like_users.add(user)
            return Response({"status": "liked", "like_count": product.like_count}, status=status.HTTP_201_CREATED)