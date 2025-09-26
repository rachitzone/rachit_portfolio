from django.urls import path
from .views import BlogListView, BlogDetailView

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
]
