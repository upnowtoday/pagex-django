from django.db import models
from django.conf import settings


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    tag = models.ManyToManyField('Tag', related_name='blog_post')

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.title


class Promote(models.Model):
    title = models.CharField(max_length=250, blank=True)
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='promotes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='promotes')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.title


class React(models.Model):
    content = models.TextField()
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='reacts')
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reacts')
    tag = models.ManyToManyField('Tag', related_name='reacts')

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return f'{self.post.title} - {self.content[:20]}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
