from rest_framework import serializers
from apps.products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
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
        # View에서 넘겨준 request 객체를 가져옵니다.
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False

class ProductDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    image_url = serializers.CharField(read_only=True, source='image.url')
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'like_users')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False