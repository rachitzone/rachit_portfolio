from rest_framework import serializers
from .models import BlogPost


class BlogPostListSerializer(serializers.ModelSerializer):
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "excerpt", "created_at"]

    def get_excerpt(self, obj: BlogPost) -> str:
        text = (obj.content or "").strip()
        return (text[:160] + ("…" if len(text) > 160 else ""))


class BlogPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "content", "created_at"]
