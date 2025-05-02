from django.core.management.base import BaseCommand
from learning.models import Resource
from django.core.files import File
from faker import Faker
import random
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Creates sample agricultural resources'

    def handle(self, *args, **options):
        fake = Faker()

        # Resource templates
        resources_data = [
            {
                "type": "guide",
                "templates": [
                    {
                        "title": "Soil Testing Guide",
                        "description": "Comprehensive guide to soil sampling and interpretation of results",
                        "filename": "soil_testing_guide.pdf"
                    },
                    {
                        "title": "Pest Management Handbook",
                        "description": "Identification and control of common agricultural pests",
                        "filename": "pest_management.pdf"
                    },
                    {
                        "title": "Organic Certification Guide",
                        "description": "Step-by-step process for organic certification",
                        "filename": "organic_certification.pdf"
                    }
                ]
            },
            {
                "type": "checklist",
                "templates": [
                    {
                        "title": "Pre-Planting Checklist",
                        "description": "Essential tasks before starting crop cultivation",
                        "filename": "preplanting_checklist.pdf"
                    },
                    {
                        "title": "Farm Safety Checklist",
                        "description": "Daily safety inspection points for farm operations",
                        "filename": "safety_checklist.pdf"
                    },
                    {
                        "title": "Harvest Readiness Checklist",
                        "description": "Indicators for optimal harvest timing",
                        "filename": "harvest_checklist.pdf"
                    }
                ]
            },
            {
                "type": "template",
                "templates": [
                    {
                        "title": "Farm Business Plan Template",
                        "description": "Customizable template for creating a farm business plan",
                        "filename": "business_plan_template.docx"
                    },
                    {
                        "title": "Crop Planning Spreadsheet",
                        "description": "Excel template for seasonal crop planning",
                        "filename": "crop_planning.xlsx"
                    },
                    {
                        "title": "Farm Record Keeping Forms",
                        "description": "Templates for maintaining farm operation records",
                        "filename": "record_keeping.pdf"
                    }
                ]
            },
            {
                "type": "document",
                "templates": [
                    {
                        "title": "Agricultural Market Report",
                        "description": "Analysis of current agricultural market trends",
                        "filename": "market_report.pdf"
                    },
                    {
                        "title": "Climate Smart Farming Guide",
                        "description": "Strategies for adapting to climate change",
                        "filename": "climate_smart_guide.pdf"
                    },
                    {
                        "title": "Farm Equipment Manual",
                        "description": "Maintenance guidelines for common farm equipment",
                        "filename": "equipment_manual.pdf"
                    }
                ]
            }
        ]

        try:
            resources_created = 0
            
            for resource_type in resources_data:
                for template in resource_type["templates"]:
                    # Create placeholder file path
                    file_path = f"placeholder_{template['filename']}"
                    
                    # Create resource
                    resource = Resource.objects.create(
                        title=template["title"],
                        description=template["description"],
                        resource_type=resource_type["type"],
                        file=file_path  # You'll need to handle actual file upload
                    )
                    
                    resources_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created resource: {resource.title}'
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {resources_created} resources'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating resources: {str(e)}')
            )