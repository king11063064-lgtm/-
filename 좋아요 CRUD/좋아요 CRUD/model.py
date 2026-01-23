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
    
    # 좋아요 기능: 유저 모델과 다대다 연결
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='like_products', 
        blank=True
    )

    def __str__(self):
        return self.name

    @property
    def like_count(self):
        return self.like_users.count()