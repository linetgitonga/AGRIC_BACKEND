from rest_framework import serializers
from .models import Course, Module, Lesson, Webinar, Resource
from accounts.serializers import UserSerializer

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('instructor',)

    def get_total_lessons(self, obj):
        return sum(module.lessons.count() for module in obj.modules.all())

class WebinarSerializer(serializers.ModelSerializer):
    speaker = UserSerializer(read_only=True)
    registered_users_count = serializers.SerializerMethodField()

    class Meta:
        model = Webinar
        fields = '__all__'
        read_only_fields = ('speaker',)

    def get_registered_users_count(self, obj):
        return obj.participants.count() if hasattr(obj, 'participants') else 0

class ResourceSerializer(serializers.ModelSerializer):
    resource_type_display = serializers.CharField(source='get_resource_type_display', read_only=True)

    class Meta:
        model = Resource
        fields = '__all__'