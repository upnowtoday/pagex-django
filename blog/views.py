from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost, React, Promote, Tag
from .serializers import (BlogPostListSerializer, ReactCreateSerializer, ReactListSerializer, PromoteEditSerializer, PromoteSerializer,
                          TagSerializer)


class MyBlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

    def get_serializer_class(self):
        return BlogPostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogPostFeedAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = BlogPost.objects.filter(author__isnull=False)
    serializer_class = BlogPostListSerializer


class ReactCRUDAPI(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method.lower() == 'get':
            return React.objects.filter(post=self.kwargs['post_id'])
        return React.objects.filter(post=self.kwargs['post_id'], author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return ReactCreateSerializer
        return ReactListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs['post_id'])


class PromoteCRUDAPI(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return PromoteEditSerializer
        return PromoteSerializer

    def get_queryset(self):
        if self.request.method.lower() == 'get':
            return Promote.objects.filter(post=self.kwargs['post_id'])
        return Promote.objects.filter(post=self.kwargs['post_id'], author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs['post_id'])


class TagAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
