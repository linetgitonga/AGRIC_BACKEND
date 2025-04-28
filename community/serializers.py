from rest_framework import serializers
from .models import Topic, Discussion, Comment, FarmingGroup
from accounts.serializers import UserSerializer

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    upvote_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',)

    def get_upvote_count(self, obj):
        return obj.upvotes.count()

class DiscussionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    upvote_count = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = '__all__'
        read_only_fields = ('author',)

    def get_upvote_count(self, obj):
        return obj.upvotes.count()

class FarmingGroupSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = FarmingGroup
        fields = '__all__'
        read_only_fields = ('creator',)

    def get_members_count(self, obj):
        return obj.members.count()