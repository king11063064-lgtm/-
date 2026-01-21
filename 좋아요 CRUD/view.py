from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# ... (기존 Product APIView들 유지) ...

class ProductLikeAPIView(APIView):
    """
    feature/PostLikeAPI: 상품 좋아요 토글 기능
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Products"],
        summary="상품 좋아요 토글 API",
        description="이미 좋아요를 누른 경우 취소하고, 누르지 않은 경우 추가합니다.",
        responses={200: {"example": {"status": "liked/unliked", "like_count": 5}}}
    )
    def post(self, request, product_id):
        # 실제 DB 연동 시 get_object_or_404 사용
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        if product.like_users.filter(id=user.id).exists():
            product.like_users.remove(user)
            return Response({"status": "unliked", "like_count": product.like_count}, status=status.HTTP_200_OK)
        else:
            product.like_users.add(user)
            return Response({"status": "liked", "like_count": product.like_count}, status=status.HTTP_201_CREATED)