from rest_framework import serializers
from apps.products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(read_only=True, source='image.url')
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'like_users')
        extra_kwargs = {
            'image': {'write_only': True},
            'stock': {'write_only': True},
            'description': {'write_only': True},
        }

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Mock 데이터 대응을 위한 예외처리 포함
            return getattr(obj, 'like_users', None) and obj.like_users.filter(id=request.user.id).exists()
        return False

# ProductDetailSerializer도 동일한 방식으로 like_count, is_liked 추가