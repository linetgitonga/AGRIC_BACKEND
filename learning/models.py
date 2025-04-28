from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/')
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Webinar(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    speaker = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    meeting_link = models.URLField()
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('guide', 'Guide'),
        ('checklist', 'Checklist'),
        ('template', 'Template'),
        ('document', 'Document'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_resource_type_display()}: {self.title}"