from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Topic, Discussion, Comment, FarmingGroup

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'topic', 'created_at', 'is_pinned')
    search_fields = ('title', 'content', 'author__email')
    list_filter = ('topic', 'is_pinned', 'created_at')
    raw_id_fields = ('author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'author', 'created_at')
    search_fields = ('content', 'author__email')
    list_filter = ('created_at',)
    raw_id_fields = ('author', 'discussion')

@admin.register(FarmingGroup)
class FarmingGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'location', 'is_private', 'created_at')
    search_fields = ('name', 'description', 'location')
    list_filter = ('is_private', 'created_at')
    raw_id_fields = ('creator',)
    filter_horizontal = ('members',)