from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    # 작성 시 현재 로그인한 유저를 작성자로 자동 저장
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)