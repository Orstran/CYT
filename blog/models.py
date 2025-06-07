from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_predefined = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    custom_category = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class About(models.Model):
    content = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Page"

class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Contact Page"

class AnimeNavigation(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='anime_images/', blank=True, null=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class WebsiteNavigation(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='images/default.png', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# 修改记录：添加了 UserProfile 模型以存储用户头像，默认使用 static/images/default.png。