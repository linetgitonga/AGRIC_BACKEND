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
            for buyer in buyers:
                BuyerPreference.objects.get_or_create(
                    buyer=buyer,
                    defaults={
                        'is_organic_preferred': random.choice([True, False]),
                        'preferred_regions': ', '.join(fake.random_choices(
                            elements=('Nairobi', 'Nakuru', 'Meru', 'Nyeri', 'Eldoret', 'Kisumu'),
                            length=random.randint(1, 3)
                        )),
                        'quantity_needed_monthly': f"{random.randint(100, 1000)} kg per month",
                        'notes': fake.text(max_nb_chars=200)
                    }
                )
                pref = BuyerPreference.objects.get(buyer=buyer)
                pref.preferred_crops.set(random.sample(list(crops), k=random.randint(2, 5)))

            # 2. Create FarmerOffers
            self.stdout.write('Creating farmer offers...')
            for _ in range(50):
                farmer = random.choice(farmers)
                crop = random.choice(crops)
                harvest_date = datetime.now() + timedelta(days=random.randint(30, 90))
                
                FarmerOffer.objects.create(
                    farmer=farmer,
                    crop=crop,
                    title=f"Premium {crop.name} Available",
                    description=fake.paragraph(),
                    quantity_available=Decimal(random.uniform(100, 1000)),
                    unit=random.choice(['kg', 'ton', 'bag']),
                    price_per_unit=Decimal(random.uniform(50, 500)),
                    is_negotiable=random.choice([True, False]),
                    harvest_date=harvest_date,
                    available_from=harvest_date,
                    available_until=harvest_date + timedelta(days=30),
                    is_organic=random.choice([True, False]),
                    quality_description=fake.paragraph(),
                    location=fake.city(),
                    status=random.choice(['available', 'withdrawn', 'sold'])
                )

            # 3. Create ContractRequests
            self.stdout.write('Creating contract requests...')
            for _ in range(40):
                buyer = random.choice(buyers)
                farmer = random.choice(farmers)
                crop = random.choice(crops)
                
                ContractRequest.objects.create(
                    buyer=buyer,
                    farmer=farmer,
                    crop=crop,
                    title=f"Contract for {crop.name} Supply",
                    description=fake.paragraph(),
                    quantity_required=Decimal(random.uniform(1000, 5000)),
                    unit=random.choice(['kg', 'ton']),
                    price_per_unit=Decimal(random.uniform(50, 200)),
                    delivery_date=datetime.now() + timedelta(days=random.randint(60, 180)),
                    delivery_location=fake.city(),
                    quality_requirements=fake.paragraph(),
                    payment_terms=f"Payment within {random.choice([7, 14, 30])} days after delivery",
                    status=random.choice(['pending', 'accepted', 'rejected', 'fulfilled']),
                    farmer_notes=fake.text(max_nb_chars=100),
                    buyer_notes=fake.text(max_nb_chars=100)
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
                        'message': fake.text(max_nb_chars=200)
                    }
                )

            # 5. Create Messages
            self.stdout.write('Creating messages...')
            # Get accepted connections
            connections = Connection.objects.filter(status='accepted')
            
            for connection in connections:
                # Create 3-7 messages for each connection
                for _ in range(random.randint(3, 7)):
                    sender = random.choice([connection.initiator, connection.receiver])
                    receiver = connection.receiver if sender == connection.initiator else connection.initiator
                    
                    Message.objects.create(
                        sender=sender,
                        receiver=receiver,
                        subject=fake.sentence(),
                        content=fake.paragraphs(nb=random.randint(1, 3)),
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