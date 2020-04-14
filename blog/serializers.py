from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import BlogPost, React, Promote, Tag

User = get_user_model()


class AuthorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class ReactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = React
        fields = ('content',)


class ReactListSerializer(serializers.ModelSerializer):
    author = AuthorShortSerializer(read_only=True)

    class Meta:
        model = React
        fields = ('id', 'content', 'author', 'created_date')


class BlogPostListSerializer(serializers.ModelSerializer):
    author = AuthorShortSerializer(read_only=True)
    reacts = ReactListSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'author', 'reacts')
        read_only_fields = ('id',)


class PromoteEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promote
        fields = ('id', 'title',)


class PromoteSerializer(serializers.ModelSerializer):
    author = AuthorShortSerializer()

    class Meta:
        model = Promote
        fields = ('id', 'title', 'post', 'author', 'created_date')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
