from rest_framework import serializers
from apps.products.models import Product, Like

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(read_only=True, source='image.url')
    like_count = serializers.IntegerField(source='like_count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('like_users', 'created_at', 'updated_at')
        extra_kwargs = {
            'image': {'write_only': True},
            'stock': {'write_only': True},
            'description': {'write_only': True},
        }

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Like 모델에서 현재 유저와 이 상품의 is_liked 상태를 확인
            like = Like.objects.filter(user=request.user, product=obj).first()
            return like.is_liked if like else False
        return False

class ProductDetailSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'like_users')