from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from learning.models import Webinar
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample agricultural webinars'

    def handle(self, *args, **options):
        fake = Faker()

        # Get expert users for speakers
        speakers = User.objects.filter(user_type='expert')
        if not speakers:
            self.stdout.write(self.style.ERROR('No expert users found. Please create expert users first.'))
            return

        # Webinar templates
        webinars_data = [
            {
                "title": "Modern Irrigation Technologies",
                "description": "Explore the latest irrigation systems and water management techniques for efficient farming",
                "duration": 60,
                "price": 999
            },
            {
                "title": "Organic Farming Certification Process",
                "description": "Step-by-step guide to obtaining organic certification for your farm",
                "duration": 90,
                "price": 1499
            },
            {
                "title": "Digital Tools for Farm Management",
                "description": "Introduction to agricultural apps and software for better farm management",
                "duration": 45,
                "price": 0
            },
            {
                "title": "Soil Health Management",
                "description": "Understanding soil testing, amendments, and maintenance for optimal crop growth",
                "duration": 75,
                "price": 799
            },
            {
                "title": "Post-Harvest Technology",
                "description": "Best practices for handling, storing, and preserving agricultural produce",
                "duration": 60,
                "price": 699
            },
            {
                "title": "Agricultural Marketing Strategies",
                "description": "Effective methods to market your farm products and increase profits",
                "duration": 120,
                "price": 1999
            },
            {
                "title": "Climate-Smart Farming Practices",
                "description": "Adapting farming methods to climate change challenges",
                "duration": 90,
                "price": 0
            },
            {
                "title": "Farm Financial Planning",
                "description": "Managing farm finances, budgeting, and securing agricultural loans",
                "duration": 120,
                "price": 1499
            }
        ]

        try:
            webinars_created = 0
            current_date = datetime.now()

            for webinar_data in webinars_data:
                # Schedule webinar in next 30 days
                scheduled_time = current_date + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(9, 16)  # Between 9 AM and 4 PM
                )

                webinar = Webinar.objects.create(
                    title=webinar_data["title"],
                    description=webinar_data["description"],
                    speaker=random.choice(speakers),
                    scheduled_time=scheduled_time,
                    duration=webinar_data["duration"],
                    meeting_link=f"https://meet.example.com/{fake.uuid4()}",
                    is_free=webinar_data["price"] == 0,
                    price=webinar_data["price"]
                )

                webinars_created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created webinar: {webinar.title} scheduled for {webinar.scheduled_time}'
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {webinars_created} webinars'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating webinars: {str(e)}')
            )