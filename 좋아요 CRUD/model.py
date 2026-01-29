from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products')
    price = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ManyToManyField에 'through' 옵션을 사용하여 상세 필드를 가진 Like 모델을 연결합니다.
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Like',
        related_name='like_products'
    )

    @property
    def like_count(self):
        return self.likes.filter(is_liked=True).count()

class Like(models.Model):
    # id 필드는 Django가 자동으로 생성합니다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes') # post_id 역할
    is_liked = models.BooleanField(default=True) # 좋아요 상태값
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 한 유저가 한 상품에 대해 하나의 좋아요만 기록하도록 제한
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} liked {self.product.name} - {self.is_liked}"