from rest_framework import generics
from .models import BlogPost
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer


class BlogListView(generics.ListAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostListSerializer


class BlogDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'
