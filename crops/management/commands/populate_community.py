from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from community.models import Topic, Discussion, Comment, FarmingGroup
import random

class Command(BaseCommand):
    help = 'Populate Topic, Discussion, Comment, and FarmingGroup models with sample data'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING('No users found. Please create at least one user.'))
            return

        # Create Topics
        topics = [
            {"name": "Crop Diseases", "description": "Discuss common crop diseases and solutions."},
            {"name": "Organic Farming", "description": "Share tips and experiences on organic farming."},
            {"name": "Market Trends", "description": "Talk about agricultural market prices and trends."},
        ]
        topic_objs = []
        for t in topics:
            obj, _ = Topic.objects.get_or_create(name=t["name"], defaults=t)
            topic_objs.append(obj)
        self.stdout.write(self.style.SUCCESS('Sample topics added.'))

        # Create Discussions
        discussions = []
        for i in range(5):
            author = random.choice(users)
            topic = random.choice(topic_objs)
            disc = Discussion.objects.create(
                title=f"Discussion {i+1} on {topic.name}",
                content=f"This is a sample discussion about {topic.name}.",
                author=author,
                topic=topic
            )
            discussions.append(disc)
        self.stdout.write(self.style.SUCCESS('Sample discussions added.'))

        # Create Comments
        for disc in discussions:
            for i in range(2):
                author = random.choice(users)
                Comment.objects.create(
                    discussion=disc,
                    author=author,
                    content=f"Sample comment {i+1} on {disc.title}."
                )
        self.stdout.write(self.style.SUCCESS('Sample comments added.'))

        # Create Farming Groups
        for i in range(3):
            creator = random.choice(users)
            group = FarmingGroup.objects.create(
                name=f"Farming Group {i+1}",
                description=f"Description for farming group {i+1}.",
                creator=creator,
                location=f"Location {i+1}",
                is_private=random.choice([True, False])
            )
            group.members.set(random.sample(users, min(len(users), random.randint(1, len(users)))))
        self.stdout.write(self.style.SUCCESS('Sample farming groups added.'))