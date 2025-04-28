from django.contrib import admin
from .models import Course, Module, Lesson, Webinar, Resource

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ['order']

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    ordering = ['order']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'duration', 'price', 'is_free', 'created_at')
    list_filter = ('is_free', 'created_at')
    search_fields = ('title', 'description', 'instructor__email')
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'duration', 'order')
    list_filter = ('module__course',)
    search_fields = ('title', 'content')

@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'scheduled_time', 'duration', 'is_free', 'price')
    list_filter = ('is_free', 'scheduled_time')
    search_fields = ('title', 'description', 'speaker__email')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'created_at')
    list_filter = ('resource_type', 'created_at')
    search_fields = ('title', 'description')