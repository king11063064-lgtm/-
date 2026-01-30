from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Exam, Like

class ExamLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Exams"],
        summary="쪽지시험 좋아요 토글",
        description="요청 시 id, user_id, post_id, is_liked 등의 상세 정보를 반환합니다."
    )
    def post(self, request, post_id):
        # 1. 대상 시험(Exam) 존재 확인
        exam = get_object_or_404(Exam, id=post_id)
        user = request.user

        # 2. 좋아요 레코드 가져오거나 생성 (Toggle 로직)
        like, created = Like.objects.get_or_create(user=user, post=exam)
        
        if not created:
            # 이미 존재하면 상태 반전
            like.is_liked = not like.is_liked
            like.save()

        # 3. 요청하신 6개 필드 기반 응답 데이터 구성
        return Response({
            "id": like.id,
            "user_id": user.id,
            "post_id": exam.id,
            "is_liked": like.is_liked,
            "created_at": like.created_at,
            "updated_at": like.updated_at
        }, status=status.HTTP_200_OK)