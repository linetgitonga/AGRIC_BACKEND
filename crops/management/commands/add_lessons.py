from django.core.management.base import BaseCommand
from django.db import transaction
from learning.models import Module, Lesson
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Creates detailed lessons for existing modules'

    def handle(self, *args, **options):
        fake = Faker()

        # Detailed lesson templates for different module types
        lesson_templates = {
            "Soil Conservation": [
                {
                    "title": "Understanding Soil Types",
                    "content": """
                    Detailed exploration of different soil types:
                    1. Sandy Soils: Characteristics and management
                    2. Clay Soils: Properties and improvement techniques
                    3. Loamy Soils: Optimal conditions and maintenance
                    4. Silt Soils: Benefits and challenges
                    
                    Practical exercises include soil texture testing and structure assessment.
                    """,
                    "video_url": "https://example.com/videos/soil-types",
                    "duration": 45
                },
                {
                    "title": "Erosion Prevention Techniques",
                    "content": """
                    Comprehensive guide to preventing soil erosion:
                    1. Contour farming methods
                    2. Terracing techniques
                    3. Windbreak implementation
                    4. Cover crop strategies
                    
                    Includes case studies from successful erosion prevention projects.
                    """,
                    "video_url": "https://example.com/videos/erosion-prevention",
                    "duration": 40
                }
            ],
            
            "Water Management": [
                {
                    "title": "Irrigation System Design",
                    "content": """
                    Complete overview of irrigation systems:
                    1. Drip irrigation setup
                    2. Sprinkler system planning
                    3. Water distribution calculations
                    4. Maintenance schedules
                    
                    Includes practical design exercises and cost analysis.
                    """,
                    "video_url": "https://example.com/videos/irrigation-design",
                    "duration": 50
                },
                {
                    "title": "Water Conservation Methods",
                    "content": """
                    Advanced water conservation techniques:
                    1. Mulching strategies
                    2. Drought-resistant farming
                    3. Water recycling systems
                    4. Soil moisture management
                    
                    Features real-world examples and efficiency calculations.
                    """,
                    "video_url": "https://example.com/videos/water-conservation",
                    "duration": 35
                }
            ],

            "Digital Farming": [
                {
                    "title": "GPS Technology in Agriculture",
                    "content": """
                    Implementation of GPS systems in farming:
                    1. Equipment guidance systems
                    2. Field mapping techniques
                    3. Yield monitoring
                    4. Variable rate applications
                    
                    Includes hands-on GPS calibration exercises.
                    """,
                    "video_url": "https://example.com/videos/gps-farming",
                    "duration": 55
                },
                {
                    "title": "Farm Management Software",
                    "content": """
                    Guide to agricultural software solutions:
                    1. Record keeping systems
                    2. Crop planning tools
                    3. Financial management software
                    4. Data analysis platforms
                    
                    Features software demonstrations and practical exercises.
                    """,
                    "video_url": "https://example.com/videos/farm-software",
                    "duration": 45
                }
            ],

            "Financial Planning": [
                {
                    "title": "Farm Budgeting",
                    "content": """
                    Comprehensive farm budget development:
                    1. Income projections
                    2. Cost estimation
                    3. Cash flow management
                    4. Risk assessment
                    
                    Includes spreadsheet templates and case studies.
                    """,
                    "video_url": "https://example.com/videos/farm-budgeting",
                    "duration": 60
                }
            ]
        }

        try:
            with transaction.atomic():
                modules = Module.objects.all()
                lessons_created = 0

                for module in modules:
                    # Get relevant lesson template or use generic template
                    module_type = next(
                        (key for key in lesson_templates.keys() if key.lower() in module.title.lower()),
                        "general"
                    )
                    
                    if module_type == "general":
                        # Generate generic lessons if no specific template exists
                        num_lessons = random.randint(3, 5)
                        for order in range(1, num_lessons + 1):
                            Lesson.objects.create(
                                module=module,
                                title=f"Lesson {order}: {fake.catch_phrase()}",
                                content="\n".join(fake.paragraphs(nb=3)),
                                video_url=f"https://example.com/videos/{fake.uuid4()}",
                                duration=random.randint(30, 60),
                                order=order
                            )
                            lessons_created += 1
                    else:
                        # Create lessons from template
                        for order, lesson_data in enumerate(lesson_templates[module_type], 1):
                            Lesson.objects.create(
                                module=module,
                                title=lesson_data["title"],
                                content=lesson_data["content"],
                                video_url=lesson_data["video_url"],
                                duration=lesson_data["duration"],
                                order=order
                            )
                            lessons_created += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created lessons for module: {module.title}'
                        )
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {lessons_created} lessons'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating lessons: {str(e)}')
            )