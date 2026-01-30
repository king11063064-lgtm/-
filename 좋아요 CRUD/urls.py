from django.urls import path
from apps.exams import views

urlpatterns = [
    # 1. 시험 전체 목록 조회 및 새로운 시험 등록
    # GET  /exams/
    # POST /exams/
    path("", views.ExamListCreateAPIView.as_view(), name="exam-list-create"),

    # 2. 특정 시험 상세 조회, 수정, 삭제
    # GET    /exams/<post_id>/
    # PUT    /exams/<post_id>/
    # DELETE /exams/<post_id>/
    path("<int:post_id>/", views.ExamRetrieveUpdateDestroyAPIView.as_view(), name="exam-detail"),

    # 3. 특정 시험 좋아요 토글 (요구하신 6개 필드 응답 API)
    # POST /exams/<post_id>/like/
    path("<int:post_id>/like/", views.ExamLikeAPIView.as_view(), name="exam-like"),
]