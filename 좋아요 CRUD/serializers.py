from rest_framework import serializers
from .models import Exam, Like

class LikeSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    post_id = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Like
        fields = ['id', 'user_id', 'post_id', 'is_liked', 'created_at', 'updated_at']

class ExamSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='like_count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        exclude = ('like_users',)

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            like = Like.objects.filter(user=request.user, post=obj).first()
            return like.is_liked if like else False
        return False