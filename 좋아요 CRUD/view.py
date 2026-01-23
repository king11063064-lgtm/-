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
    
    @extend_schema(tags=["Products"], summary="상품 목록 조회")
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')
        # context 전달 필수
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
        # context 전달 필수
        serializer = self.serializer_class(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Products"], summary="상품 좋아요 토글")
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        if product.like_users.filter(id=user.id).exists():
            product.like_users.remove(user)
            return Response({"status": "unliked", "like_count": product.like_count}, status=200)
        else:
            product.like_users.add(user)
            return Response({"status": "liked", "like_count": product.like_count}, status=201)