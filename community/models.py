from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Discussion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name='upvoted_discussions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    upvotes = models.ManyToManyField(User, related_name='upvoted_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.email} on {self.discussion.title}"

class FarmingGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='farming_groups')
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name