from rest_framework import routers
from django.urls import path
from blog import views

drf_router = routers.DefaultRouter()
drf_router.register('my-post', views.MyBlogPostViewSet, basename='my-blog-post')
drf_router.register(r'feed/(?P<post_id>[0-9]+)/react', views.ReactCRUDAPI, basename='post-react')
drf_router.register(r'feed/(?P<post_id>[0-9]+)/promote', views.PromoteCRUDAPI, basename='post-promote')

urlpatterns = [
                  path('feed/', views.BlogPostFeedAPI.as_view(), name='blog-feed'),
                  path('tag/', views.TagAPI.as_view(), name='tags'),
              ] + drf_router.urls
