from django.core.management.base import BaseCommand
from learning.models import Course, Module, Lesson
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates sample modules and lessons for agricultural courses'

    def handle(self, *args, **options):
        # Comprehensive module templates

        course_modules = {
            "Sustainable Farming Practices": [
                {
                    "title": "Introduction to Sustainable Agriculture",
                    "description": "Foundation concepts of sustainable farming",
                    "lessons": [
                        {
                            "title": "What is Sustainable Agriculture?",
                            "content": "Overview of sustainable farming principles and practices...",
                            "duration": 30,
                            "video_url": "https://example.com/videos/intro-sustainable-ag"
                        },
                        {
                            "title": "Environmental Impact Assessment",
                            "content": "Methods to evaluate farming's environmental impact...",
                            "duration": 45
                        }
                    ]
                },
                {
                    "title": "Soil Fertility Management",
                    "description": "Understanding and maintaining soil fertility",
                    "lessons": [
                        {
                            "title": "Soil Testing Fundamentals",
                            "content": "Methods and importance of regular soil testing...",
                            "duration": 40,
                            "video_url": "https://example.com/videos/soil-testing"
                        },
                        {
                            "title": "Organic Matter Management",
                            "content": "Techniques for building and maintaining soil organic matter...",
                            "duration": 35
                        }
                    ]
                }
            ],
            "Regenerative Agriculture": [
                {
                    "title": "Digital Farming Tools",
                    "description": "Introduction to modern agricultural technology",
                    "lessons": [
                        {
                            "title": "GPS and Precision Agriculture",
                            "content": "Using GPS technology for precise farming operations...",
                            "duration": 45,
                            "video_url": "https://example.com/videos/gps-farming"
                        },
                        {
                            "title": "Farm Management Software",
                            "content": "Overview of digital tools for farm management...",
                            "duration": 50
                        }
                    ]
                }
            ],
            "Crop Disease Management": [
                {
                    "title": "Disease Identification",
                    "description": "Methods to identify and diagnose crop diseases",
                    "lessons": [
                        {
                            "title": "Common Disease Symptoms",
                            "content": "Visual identification of major crop diseases...",
                            "duration": 40,
                            "video_url": "https://example.com/videos/disease-symptoms"
                        },
                        {
                            "title": "Disease Prevention Strategies",
                            "content": "Preventive measures and best practices...",
                            "duration": 35
                        }
                    ]
                }
            ],

            "Precision Farming Technologies":[
                {
                    "title": "Introduction to Precision Agriculture",
                    "description": "Understanding the principles and technologies of precision farming",
                    "lessons": [
                        {
                            "title": "What is Precision Agriculture?",
                            "content": "Overview of precision agriculture concepts and benefits...",
                            "duration": 30,
                            "video_url": "https://example.com/videos/intro-precision-ag"
                        },
                        {
                            "title": "Technologies in Precision Farming",
                            "content": "Exploring the tools and technologies used in precision agriculture...",
                            "duration": 45
                        },
                        {
                            "title": "Auto-Steer Systems",
                            "content": "Implementing GPS-guided equipment for field operations",
                            "duration": 50,
                            "video_url": "https://example.com/videos/gps-farming"
                        },
                        {
                            "title": "Yield Mapping",
                            "content": "Collecting and analyzing spatial yield data",
                            "duration": 45
                        }
                    ]
                }

            ],

            "Aquaponics Systems": [
                {
                    "title": "Introduction to Sensor Technology",
                    "description": "Understanding the role of sensors in modern agriculture",
                    "lessons": [
                         {
                            "title": "Soil Moisture Sensors",
                            "content": "Installing and interpreting soil moisture data",
                            "duration": 40,
                            "video_url": "https://example.com/videos/soil-sensors"
                        },
                        {
                            "title": "Types of Agricultural Sensors",
                            "content": "Overview of different sensor types and their applications...",
                            "duration": 30,
                            "video_url": "https://example.com/videos/sensor-types"
                        },
                        {
                            "title": "Data Collection and Analysis",
                            "content": "Methods for collecting and interpreting sensor data...",
                            "duration": 45
                        },
                         {
                            "title": "Drone Scouting",
                            "content": "Using aerial imagery for crop health assessment",
                            "duration": 55
                        }
                    ]
                }
            ],
            "Post-Harvest Technology": [
                {
                    "title": "Storage Solutions",
                    "description": "Maintaining quality after harvest",
                    "lessons": [
                        {
                            "title": "Cold Chain Management",
                            "content": "Temperature control from field to market",
                            "duration": 50,
                            "video_url": "https://example.com/videos/cold-chain"
                        },
                        {
                            "title": "Modified Atmosphere",
                            "content": "Using gas mixtures to extend shelf life",
                            "duration": 45
                        }
                    ]
                }
            ]

        }

        # Add these new modules to your existing course_modules dictionary
        course_modules.update({
            "Financial Management for Farmers": [
                {
                    "title": "Farm Financial Planning",
                    "description": "Essential financial management skills for farmers",
                    "lessons": [
                        {
                            "title": "Farm Budgeting Basics",
                            "content": "Creating and managing farm budgets, cash flow planning...",
                            "duration": 45,
                            "video_url": "https://example.com/videos/farm-budgeting"
                        },
                        {
                            "title": "Record Keeping Systems",
                            "content": "Digital and manual systems for financial record keeping...",
                            "duration": 40
                        },
                        {
                            "title": "Agricultural Tax Planning",
                            "content": "Understanding tax obligations and deductions for farmers...",
                            "duration": 50
                        }
                    ]
                },
                {
                    "title": "Agricultural Financing",
                    "description": "Understanding farm credit and loan options",
                    "lessons": [
                        {
                            "title": "Farm Loan Types",
                            "content": "Overview of different agricultural loan options...",
                            "duration": 35,
                            "video_url": "https://example.com/videos/farm-loans"
                        },
                        {
                            "title": "Grant Opportunities",
                            "content": "Finding and applying for agricultural grants...",
                            "duration": 45
                        }
                    ]
                }
            ],
            
            "Organic Farming Certification": [
                {
                    "title": "Certification Requirements",
                    "description": "Understanding organic certification standards",
                    "lessons": [
                        {
                            "title": "Organic Standards Overview",
                            "content": "Key requirements for organic certification...",
                            "duration": 40,
                            "video_url": "https://example.com/videos/organic-standards"
                        },
                        {
                            "title": "Record Keeping for Certification",
                            "content": "Documentation requirements and systems...",
                            "duration": 35
                        }
                    ]
                },
                {
                    "title": "Organic Practices",
                    "description": "Implementing organic farming methods",
                    "lessons": [
                        {
                            "title": "Natural Pest Management",
                            "content": "Organic pest control strategies...",
                            "duration": 45,
                            "video_url": "https://example.com/videos/organic-pest-control"
                        },
                        {
                            "title": "Soil Fertility Management",
                            "content": "Building soil health organically...",
                            "duration": 50
                        }
                    ]
                }
            ],

            "Livestock Health Management": [
                {
                    "title": "Animal Health Basics",
                    "description": "Fundamental livestock healthcare practices",
                    "lessons": [
                        {
                            "title": "Health Monitoring",
                            "content": "Daily health check procedures and vital signs...",
                            "duration": 40,
                            "video_url": "https://example.com/videos/livestock-health"
                        },
                        {
                            "title": "Vaccination Programs",
                            "content": "Essential vaccinations and scheduling...",
                            "duration": 45
                        }
                    ]
                },
                {
                    "title": "Disease Prevention",
                    "description": "Preventive healthcare measures",
                    "lessons": [
                        {
                            "title": "Biosecurity Measures",
                            "content": "Implementing farm biosecurity protocols...",
                            "duration": 50,
                            "video_url": "https://example.com/videos/biosecurity"
                        },
                        {
                            "title": "Nutrition Management",
                            "content": "Feed quality and nutritional requirements...",
                            "duration": 40
                        }
                    ]
                }
            ],

            "Agricultural Value Addition": [
                {
                    "title": "Product Processing",
                    "description": "Basic food processing techniques",
                    "lessons": [
                        {
                            "title": "Processing Methods",
                            "content": "Different processing techniques for farm products...",
                            "duration": 45,
                            "video_url": "https://example.com/videos/food-processing"
                        },
                        {
                            "title": "Quality Standards",
                            "content": "Maintaining quality in processed products...",
                            "duration": 40
                        }
                    ]
                },
                {
                    "title": "Marketing Value-Added Products",
                    "description": "Strategies for marketing processed products",
                    "lessons": [
                        {
                            "title": "Market Research",
                            "content": "Identifying market opportunities...",
                            "duration": 35,
                            "video_url": "https://example.com/videos/market-research"
                        },
                        {
                            "title": "Branding and Packaging",
                            "content": "Creating appealing product presentations...",
                            "duration": 40
                        }
                    ]
                }
            ],

            "Climate-Smart Agriculture": [
                {
                    "title": "Climate Adaptation",
                    "description": "Adapting farming to climate change",
                    "lessons": [
                        {
                            "title": "Climate Risk Assessment",
                            "content": "Evaluating climate risks for your farm...",
                            "duration": 45,
                            "video_url": "https://example.com/videos/climate-risk"
                        },
                        {
                            "title": "Adaptation Strategies",
                            "content": "Implementing climate-resilient practices...",
                            "duration": 50
                        }
                    ]
                },
                {
                    "title": "Carbon Farming",
                    "description": "Reducing carbon footprint in agriculture",
                    "lessons": [
                        {
                            "title": "Carbon Sequestration",
                            "content": "Practices that increase soil carbon storage...",
                            "duration": 40,
                            "video_url": "https://example.com/videos/carbon-farming"
                        },
                        {
                            "title": "Emission Reduction",
                            "content": "Strategies to reduce farm emissions...",
                            "duration": 45
                        }
                    ]
                }
            ]
        })
      

        try:
            with transaction.atomic():
                courses = Course.objects.all()
                modules_created = 0
                lessons_created = 0

                for course in courses:
                    # Get modules for this course type or use default modules
                    modules_data = course_modules.get(course.title, course_modules["Sustainable Farming Practices"])
                    
                    for order, module_data in enumerate(modules_data, 1):
                        # Create module
                        module = Module.objects.create(
                            course=course,
                            title=module_data["title"],
                            description=module_data["description"],
                            order=order
                        )
                        modules_created += 1

                        # Create lessons for this module
                        for lesson_order, lesson_data in enumerate(module_data["lessons"], 1):
                            Lesson.objects.create(
                                module=module,
                                title=lesson_data["title"],
                                content=lesson_data["content"],
                                video_url=lesson_data.get("video_url", ""),
                                duration=lesson_data["duration"],
                                order=lesson_order
                            )
                            lessons_created += 1

                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created module "{module.title}" with {len(module_data["lessons"])} lessons'
                            )
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {modules_created} modules with {lessons_created} lessons'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating modules: {str(e)}')
            )