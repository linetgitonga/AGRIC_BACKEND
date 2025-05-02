from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from learning.models import Course, Module, Lesson
from faker import Faker
import random
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates 30 detailed agricultural courses with modules and lessons'

    def handle(self, *args, **options):
        fake = Faker()

        # Get instructors (agriculture experts)
        instructors = User.objects.filter(user_type='expert')
        if not instructors:
            self.stdout.write(self.style.ERROR('No expert users found. Please create expert users first.'))
            return

        # Detailed course data
        courses_data = [

            {
                "title": "Sustainable Agriculture Practices",
                "description": "Eco-friendly farming methods for long-term productivity",
                "modules": [
                    {
                        "title": "Soil Conservation",
                        "lessons": [
                            "Crop Rotation Techniques",
                            "Cover Cropping Benefits",
                            "Reducing Soil Erosion"
                        ]
                    },
                    {
                        "title": "Water Management",
                        "lessons": [
                            "Drip Irrigation Systems",
                            "Rainwater Harvesting",
                            "Water Conservation Methods"
                        ]
                    }
                ]
            },
            {
                "title": "Organic Farming Certification",
                "description": "Complete guide to organic certification processes",
                "modules": [
                    {
                        "title": "Certification Standards",
                        "lessons": [
                            "International Organic Standards",
                            "Documentation Requirements",
                            "Inspection Procedures"
                        ]
                    },
                    {
                        "title": "Organic Inputs",
                        "lessons": [
                            "Approved Pest Control Methods",
                            "Organic Fertilizer Production",
                            "Non-GMO Seed Selection"
                        ]
                    }
                ]
            },
            {
                "title": "Precision Farming Technologies",
                "description": "Leveraging technology for efficient farm management",
                "modules": [
                    {
                        "title": "Digital Tools",
                        "lessons": [
                            "GPS-Guided Equipment",
                            "Soil Sensors and Monitoring",
                            "Farm Management Software"
                        ]
                    },
                    {
                        "title": "Data Analysis",
                        "lessons": [
                            "Yield Mapping Interpretation",
                            "Variable Rate Technology",
                            "Weather Data Integration"
                        ]
                    }
                ]
            },
            {
                "title": "Agribusiness Marketing",
                "description": "Strategies for profitable farm product marketing",
                "modules": [
                    {
                        "title": "Market Channels",
                        "lessons": [
                            "Direct-to-Consumer Sales",
                            "Wholesale Market Strategies",
                            "Export Market Requirements"
                        ]
                    },
                    {
                        "title": "Brand Development",
                        "lessons": [
                            "Product Differentiation",
                            "Packaging for Market Appeal",
                            "Digital Marketing for Farmers"
                        ]
                    }
                ]
            },

            {
                "title": "Integrated Pest Management",
                "description": "Holistic approach to pest control",
                "modules": [
                    {
                        "title": "Prevention Methods",
                        "lessons": [
                            "Beneficial Insect Habitat",
                            "Cultural Control Practices",
                            "Resistant Crop Varieties"
                        ]
                    },
                    {
                        "title": "Intervention Strategies",
                        "lessons": [
                            "Biological Control Agents",
                            "Targeted Pesticide Use",
                            "Monitoring and Thresholds"
                        ]
                    }
                ]
            },
            {
                "title": "Greenhouse Production",
                "description": "Year-round controlled environment agriculture",
                "modules": [
                    {
                        "title": "Structure Design",
                        "lessons": [
                            "Greenhouse Types Comparison",
                            "Ventilation Systems",
                            "Energy Efficiency"
                        ]
                    },
                    {
                        "title": "Crop Management",
                        "lessons": [
                            "Climate Control Systems",
                            "Hydroponic Integration",
                            "Pest Management in Enclosed Spaces"
                        ]
                    }
                ]
            },
            {
                "title": "Livestock Health Management",
                "description": "Comprehensive animal health practices",
                "modules": [
                    {
                        "title": "Preventive Care",
                        "lessons": [
                            "Vaccination Schedules",
                            "Parasite Control",
                            "Nutrition for Disease Resistance"
                        ]
                    },
                    {
                        "title": "Disease Identification",
                        "lessons": [
                            "Common Livestock Ailments",
                            "Biosecurity Measures",
                            "Zoonotic Disease Prevention"
                        ]
                    }
                ]
            },
            {
                "title": "Agricultural Value Addition",
                "description": "Transforming raw produce into higher-value products",
                "modules": [
                    {
                        "title": "Processing Techniques",
                        "lessons": [
                            "Basic Food Preservation",
                            "Small-Scale Processing Equipment",
                            "Quality Control Standards"
                        ]
                    },
                    {
                        "title": "Product Development",
                        "lessons": [
                            "Market Research for Value-Added Products",
                            "Packaging and Labeling",
                            "Shelf-Life Extension Methods"
                        ]
                    }
                ]
            },

            {
                "title": "Climate-Smart Agriculture",
                "description": "Adapting to changing climate conditions",
                "modules": [
                    {
                        "title": "Adaptation Strategies",
                        "lessons": [
                            "Drought-Resistant Crops",
                            "Weather Pattern Analysis",
                            "Microclimate Management"
                        ]
                    },
                    {
                        "title": "Mitigation Practices",
                        "lessons": [
                            "Carbon Sequestration Techniques",
                            "Reducing Farm Emissions",
                            "Renewable Energy Integration"
                        ]
                    }
                ]
            },
            {
                "title": "Farm Equipment Maintenance",
                "description": "Proper care and repair of agricultural machinery",
                "modules": [
                    {
                        "title": "Preventive Maintenance",
                        "lessons": [
                            "Service Schedules",
                            "Lubrication Points",
                            "Winterization Procedures"
                        ]
                    },
                    {
                        "title": "Troubleshooting",
                        "lessons": [
                            "Common Mechanical Issues",
                            "Electrical System Basics",
                            "Hydraulic System Maintenance"
                        ]
                    }
                ]
            },


            {
                "title": "Sustainable Farming Practices",
                "description": "Comprehensive guide to environmentally conscious farming methods",
                "modules": [
                    {
                        "title": "Soil Conservation Techniques",
                        "lessons": ["Soil Testing and Analysis", "Erosion Prevention", "Crop Rotation Planning"]
                    },
                    {
                        "title": "Water Management",
                        "lessons": ["Irrigation Systems", "Water Conservation", "Rainwater Harvesting"]
                    },
                    {
                        "title": "Organic Farming Methods",
                        "lessons": ["Natural Pest Control", "Composting", "Organic Certification"]
                    }
                ]
            },
            {
                "title": "Modern Agricultural Technology",
                "description": "Introduction to precision farming and agricultural technology",
                "modules": [
                    {
                        "title": "Precision Agriculture Basics",
                        "lessons": ["GPS Technology", "Drone Applications", "Soil Sensors"]
                    },
                    {
                        "title": "Smart Irrigation Systems",
                        "lessons": ["Automated Systems", "Moisture Monitoring", "Weather Integration"]
                    }
                ]
            },
            {
                "title": "Crop Disease Management",
                "description": "Identifying and managing common crop diseases",
                "modules": [
                    {
                        "title": "Disease Identification",
                        "lessons": ["Common Symptoms", "Diagnostic Tools", "Laboratory Testing"]
                    },
                    {
                        "title": "Treatment Methods",
                        "lessons": ["Chemical Controls", "Biological Controls", "Cultural Practices"]
                    }
                ]
            },
                        {
                "title": "Financial Management for Farmers",
                "description": "Essential financial skills for successful farm management",
                "modules": [
                    {
                        "title": "Basic Farm Accounting",
                        "lessons": [
                            "Record Keeping Basics",
                            "Understanding Cash Flow",
                            "Profit and Loss Statements"
                      ]
            },
            {
                "title": "Investment Planning",
                "lessons": [
                    "Equipment Investment Analysis",
                    "Land Acquisition Strategy",
                    "Funding and Loans"
                ]
            }
                ]
            },
            {
                "title": "Post-Harvest Technology",
                "description": "Modern techniques for post-harvest handling and storage",
                "modules": [
                    {
                        "title": "Storage Solutions",
                        "lessons": [
                            "Temperature Control",
                            "Humidity Management",
                            "Storage Facility Design"
                        ]
                    },
                    {
                        "title": "Quality Maintenance",
                        "lessons": [
                            "Grading Systems",
                            "Packaging Methods",
                            "Transportation Best Practices"
                        ]
                    }
                ]
            },

            {
                "title": "Aquaponics Systems",
                "description": "Combining fish farming with hydroponic plant production",
                "modules": [
                    {
                        "title": "System Design",
                        "lessons": [
                            "Component Selection",
                            "Water Chemistry Basics",
                            "System Cycling Process"
                        ]
                    },
                    {
                        "title": "Production Management",
                        "lessons": [
                            "Fish Feeding Strategies",
                            "Plant Nutrient Requirements",
                            "Disease Prevention in Closed Systems"
                        ]
                    }
                ]
            },

            {
                "title": "Agri-Tourism Development",
                "description": "Creating profitable farm visitor experiences",
                "modules": [
                    {
                        "title": "Experience Design",
                        "lessons": [
                            "Farm Stay Operations",
                            "Educational Activities",
                            "Seasonal Event Planning"
                        ]
                    },
                    {
                        "title": "Marketing and Safety",
                        "lessons": [
                            "Online Promotion Strategies",
                            "Liability Considerations",
                            "Visitor Flow Management"
                        ]
                    }
                ]
            },

            {
                "title": "Regenerative Agriculture",
                "description": "Farming methods that restore ecosystem health",
                "modules": [
                    {
                        "title": "Soil Regeneration",
                        "lessons": [
                            "No-Till Practices",
                            "Compost Tea Applications",
                            "Biochar Integration"
                        ]
                    },
                    {
                        "title": "Biodiversity Enhancement",
                        "lessons": [
                            "Polyculture Systems",
                            "Agroforestry Basics",
                            "Wildlife Corridor Design"
                        ]
                    }
                ]
            },

            {
                "title": "Soil Fertility Management",
                "description": "Enhancing soil health for better crop yields",
                "modules": [
                    {
                        "title": "Nutrient Management",
                        "lessons": [
                            "Soil Testing Procedures",
                            "Fertilizer Application Techniques",
                            "Organic Amendments"
                        ]
                    },
                    {
                        "title": "Soil Health Indicators",
                        "lessons": [
                            "Microbial Activity Assessment",
                            "Soil Structure Evaluation",
                            "pH and Electrical Conductivity"
                        ]
                    }
                ]
            },
            {
                "title": "Farm Safety and Risk Management",
                "description": "Ensuring safety on the farm and managing risks",
                "modules": [
                    {
                        "title": "Safety Protocols",
                        "lessons": [
                            "Personal Protective Equipment (PPE)",
                            "Emergency Response Plans",
                            "Equipment Safety Checks"
                        ]
                    },
                    {
                        "title": "Risk Assessment",
                        "lessons": [
                            "Identifying Hazards",
                            "Mitigation Strategies",
                            "Insurance Options for Farmers"
                        ]
                    }
                ]
            },
            # Add more courses here...
        ]

        # Course category tags for better organization
        categories = [
            "Crop Management", "Livestock", "Soil Science", "Farm Economics",
            "Agricultural Technology", "Organic Farming", "Pest Control",
            "Water Management", "Sustainable Agriculture", "Post-Harvest"
        ]

        try:
            courses_created = 0
            for course_data in courses_data:
                # Create course
                course = Course.objects.create(
                    title=course_data["title"],
                    description=course_data["description"],
                    instructor=random.choice(instructors),
                    duration=random.randint(300, 1200),  # 5-20 hours
                    price=random.choice([0, 499, 999, 1499, 1999]),
                    is_free=random.random() < 0.2,  # 20% chance of being free
                )

                # Create modules
                for index, module_data in enumerate(course_data["modules"], 1):
                    module = Module.objects.create(
                        course=course,
                        title=module_data["title"],
                        description=fake.paragraph(),
                        order=index
                    )

                    # Create lessons for each module
                    for lesson_index, lesson_title in enumerate(module_data["lessons"], 1):
                        Lesson.objects.create(
                            module=module,
                            title=lesson_title,
                            content="\n\n".join(fake.paragraphs(nb=3)),
                            video_url=f"https://example.com/videos/{fake.uuid4()}",
                            duration=random.randint(15, 45),  # 15-45 minutes
                            order=lesson_index
                        )

                courses_created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created course: {course.title} with {len(course_data["modules"])} modules'
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {courses_created} courses with detailed modules and lessons'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating courses: {str(e)}')
            )

