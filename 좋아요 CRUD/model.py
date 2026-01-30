from django.db import models
from django.conf import settings

class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='exams')
    time_limit = models.IntegerField(default=30)
    pass_score = models.IntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Like',
        related_name='like_exams'
    )

    @property
    def like_count(self):
        return self.likes.filter(is_liked=True).count()

class Like(models.Model):
    # id는 Django가 자동 생성 (Primary Key)
    
    # user_id 필드명 강제 지정
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        db_column='user_id'
    )
    
    # post_id 필드명 강제 지정 (Exam 객체를 가리킴)
    post = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        related_name='likes', 
        db_column='post_id'
    )
    
    is_liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')