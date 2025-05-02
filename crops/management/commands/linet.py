from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from connections.models import (
    ContractRequest, BuyerPreference, FarmerOffer,
    Connection, Message
)
from crops.models import Crop
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample data for connections and related models'

    def handle(self, *args, **options):
        fake = Faker()

        # Get admin user for special messages
        admin_email = "linetgitonga55@gmail.com"
        admin_user = User.objects.filter(email=admin_email).first()

        # Get users by type
        buyers = User.objects.filter(user_type='buyer')
        farmers = User.objects.filter(user_type='farmer')
        crops = Crop.objects.all()

        if not buyers or not farmers or not crops:
            self.stdout.write(
                self.style.ERROR('Please ensure you have buyers, farmers, and crops in the database')
            )
            return

        try:
            # 1. Create BuyerPreferences
            self.stdout.write('Creating buyer preferences...')
            kenya_regions = [
                'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 
                'Nyeri', 'Meru', 'Thika', 'Machakos', 'Kitale', 
                'Malindi', 'Kericho', 'Garissa', 'Lamu'
            ]

            for buyer in buyers:
                BuyerPreference.objects.get_or_create(
                    buyer=buyer,
                    defaults={
                        'is_organic_preferred': random.choice([True, False]),
                        'preferred_regions': ', '.join(random.sample(kenya_regions, k=random.randint(2, 4))),
                        'quantity_needed_monthly': f"{random.randint(100, 5000)} kg per month",
                        'notes': fake.paragraph(nb_sentences=3),
                        'budget_range': f"KES {random.randint(50000, 500000)} - {random.randint(500001, 1000000)}",
                        'preferred_delivery_schedule': random.choice([
                            'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly', 'On demand'
                        ])
                    }
                )
                pref = BuyerPreference.objects.get(buyer=buyer)
                pref.preferred_crops.set(random.sample(list(crops), k=random.randint(2, 5)))

            # 2. Create FarmerOffers
            self.stdout.write('Creating farmer offers...')
            offer_titles = [
                "Premium {crop} Direct from Farm",
                "Organic {crop} Available",
                "Wholesale {crop} Supply",
                "Fresh {crop} for Commercial Buyers",
                "High-Quality {crop} Harvest",
                "Bulk {crop} Available"
            ]

            for _ in range(50):
                farmer = random.choice(farmers)
                crop = random.choice(crops)
                harvest_date = datetime.now() + timedelta(days=random.randint(30, 90))
                
                FarmerOffer.objects.create(
                    farmer=farmer,
                    crop=crop,
                    title=random.choice(offer_titles).format(crop=crop.name.title()),
                    description="\n".join([
                        fake.paragraph(),
                        f"Quality: {random.choice(['Grade A', 'Premium', 'Export Quality', 'Standard'])}",
                        f"Storage: {random.choice(['Cold Storage Available', 'Warehouse Facility', 'On-farm Storage'])}"
                    ]),
                    quantity_available=Decimal(random.uniform(100, 5000)).quantize(Decimal("0.01")),
                    unit=random.choice(['kg', 'ton', 'bag']),
                    price_per_unit=Decimal(random.uniform(50, 500)).quantize(Decimal("0.01")),
                    is_negotiable=random.choice([True, False]),
                    harvest_date=harvest_date,
                    available_from=harvest_date,
                    available_until=harvest_date + timedelta(days=random.randint(30, 90)),
                    is_organic=random.choice([True, False]),
                    quality_description="\n".join([
                        "Quality Specifications:",
                        f"- Size: {random.choice(['Small', 'Medium', 'Large', 'Mixed'])}",
                        f"- Grade: {random.choice(['A', 'B', 'Premium'])}",
                        f"- Packaging: {random.choice(['Boxes', 'Bags', 'Crates', 'Bulk'])}"
                    ]),
                    location=random.choice(kenya_regions),
                    status=random.choice(['available', 'pending', 'sold'])
                )

            # 3. Create ContractRequests
            self.stdout.write('Creating contract requests...')
            contract_titles = [
                "Long-term {crop} Supply Contract",
                "Seasonal {crop} Purchase Agreement",
                "Commercial {crop} Supply Contract",
                "Premium {crop} Purchase Contract"
            ]

            for _ in range(40):
                buyer = random.choice(buyers)
                farmer = random.choice(farmers)
                crop = random.choice(crops)
                duration_months = random.randint(3, 24)
                
                ContractRequest.objects.create(
                    buyer=buyer,
                    farmer=farmer,
                    crop=crop,
                    title=random.choice(contract_titles).format(crop=crop.name.title()),
                    description="\n".join([
                        fake.paragraph(),
                        f"Contract Duration: {duration_months} months",
                        f"Quality Requirements: {random.choice(['Export Grade', 'Local Market Grade', 'Processing Grade'])}",
                        "Terms negotiable"
                    ]),
                    quantity_required=Decimal(random.uniform(1000, 10000)).quantize(Decimal("0.01")),
                    unit=random.choice(['kg', 'ton']),
                    price_per_unit=Decimal(random.uniform(50, 300)).quantize(Decimal("0.01")),
                    delivery_date=datetime.now() + timedelta(days=random.randint(60, 180)),
                    delivery_location=random.choice(kenya_regions),
                    quality_requirements="\n".join([
                        "Required Specifications:",
                        f"- Minimum Size: {random.choice(['Small', 'Medium', 'Large'])}",
                        f"- Grade Required: {random.choice(['A', 'B', 'Premium'])}",
                        f"- Certification: {random.choice(['None', 'GlobalGAP', 'Organic', 'Fair Trade'])}"
                    ]),
                    payment_terms=f"Payment within {random.choice([7, 14, 30])} days after delivery",
                    status=random.choice(['pending', 'accepted', 'rejected', 'fulfilled']),
                    farmer_notes=fake.paragraph(),
                    buyer_notes=fake.paragraph()
                )

            # 4. Create Connections
            self.stdout.write('Creating connections...')
            for _ in range(30):
                initiator = random.choice(buyers if random.random() < 0.5 else farmers)
                receiver_pool = farmers if initiator in buyers else buyers
                receiver = random.choice(receiver_pool)
                
                Connection.objects.get_or_create(
                    initiator=initiator,
                    receiver=receiver,
                    defaults={
                        'status': random.choice(['pending', 'accepted', 'rejected']),
                        'message': fake.paragraph()
                    }
                )

            # 5. Create Messages
            self.stdout.write('Creating messages...')
            message_templates = [
                "Interested in your {crop} offer. Can we discuss pricing?",
                "Looking for regular supply of {crop}. Are you available?",
                "What's the best price for bulk {crop} purchase?",
                "Can you deliver {crop} to {location}?",
                "Is the {crop} certified organic?",
                "When is your next {crop} harvest?"
            ]

            # Create messages for accepted connections
            connections = Connection.objects.filter(status='accepted')
            
            for connection in connections:
                # Create conversation thread
                for _ in range(random.randint(3, 7)):
                    sender = random.choice([connection.initiator, connection.receiver])
                    receiver = connection.receiver if sender == connection.initiator else connection.initiator
                    crop = random.choice(crops)
                    
                    Message.objects.create(
                        sender=sender,
                        receiver=receiver,
                        subject=f"Re: {crop.name} Supply",
                        content=random.choice(message_templates).format(
                            crop=crop.name,
                            location=random.choice(kenya_regions)
                        ),
                        is_read=random.choice([True, False])
                    )

            # Add admin messages if admin user exists
            if admin_user:
                self.stdout.write('Creating admin messages...')
                admin_messages = [
                    {
                        "subject": "Welcome to AgriLink",
                        "content": "Thank you for joining our platform. We're here to help you connect with agricultural partners."
                    },
                    {
                        "subject": "New Features Available",
                        "content": "We've added new features to help you manage your agricultural connections better."
                    },
                    {
                        "subject": "Market Opportunity Alert",
                        "content": "New buying opportunities available in your region. Check the marketplace!"
                    }
                ]

                for message_data in admin_messages:
                    for receiver in random.sample(list(buyers) + list(farmers), k=5):
                        Message.objects.create(
                            sender=admin_user,
                            receiver=receiver,
                            subject=message_data["subject"],
                            content=message_data["content"],
                            is_read=random.choice([True, False])
                        )

            self.stdout.write(self.style.SUCCESS(
                'Successfully created sample connection data:\n'
                f'- Buyer Preferences: {BuyerPreference.objects.count()}\n'
                f'- Farmer Offers: {FarmerOffer.objects.count()}\n'
                f'- Contract Requests: {ContractRequest.objects.count()}\n'
                f'- Connections: {Connection.objects.count()}\n'
                f'- Messages: {Message.objects.count()}'
            ))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating connection data: {str(e)}')
            )