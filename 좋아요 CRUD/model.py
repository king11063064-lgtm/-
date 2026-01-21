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
    
    # --- feature/PostLikeAPI 브랜치에서 추가된 '좋아요' 필드 ---
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='like_products', 
        blank=True
    )

    # 객체 이름을 관리자 페이지 등에서 확인하기 위한 설정
    def __str__(self):
        return self.name

    # 좋아요 개수를 쉽게 가져오기 위한 계산 속성 (Property)
    @property
    def like_count(self):
        return self.like_users.count()