from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Order, OrderItem, Product
from faker import Faker
import random
from decimal import Decimal
from datetime import datetime, timedelta
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates 100 test orders with items'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Get all buyers and farmers
        buyers = User.objects.filter(user_type='buyer')
        products = Product.objects.filter(status='available')

        if not buyers:
            self.stdout.write(self.style.ERROR('No buyers found. Please create some buyers first.'))
            return

        if not products:
            self.stdout.write(self.style.ERROR('No available products found. Please create some products first.'))
            return

        # Kenya locations
        kenya_cities = [
            'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 
            'Kitale', 'Garissa', 'Kakamega', 'Nyeri'
        ]

        # Payment statuses with weights
        payment_statuses = ['paid', 'pending', 'failed', 'refunded']
        payment_weights = [0.7, 0.2, 0.05, 0.05]  # 70% paid, 20% pending, etc.

        # Order statuses based on payment status
        status_mapping = {
            'paid': ['delivered', 'shipped', 'processing', 'confirmed'],
            'pending': ['pending'],
            'failed': ['cancelled'],
            'refunded': ['cancelled']
        }

        self.stdout.write('Creating orders...')

        try:
            for i in range(100):
                # Generate random order data
                buyer = random.choice(buyers)
                city = random.choice(kenya_cities)
                payment_status = random.choices(payment_statuses, payment_weights)[0]
                
                # Create order
                order = Order.objects.create(
                    buyer=buyer,
                    order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                    status=random.choice(status_mapping[payment_status]),
                    payment_status=payment_status,
                    shipping_address=fake.street_address(),
                    shipping_city=city,
                    shipping_state=fake.state(),
                    shipping_zip=fake.postcode(),
                    shipping_country='Kenya',
                    contact_phone=f"+254{random.randint(700000000, 799999999)}",
                    contact_email=buyer.email,
                    total_amount=Decimal('0.00'),
                    shipping_cost=Decimal(random.uniform(200, 1000)),
                    notes=fake.text(max_nb_chars=200) if random.random() > 0.7 else None,
                    created_at=datetime.now() - timedelta(days=random.randint(0, 60))
                )

                # Add 1-5 items to order
                num_items = random.randint(1, 5)
                total_amount = Decimal('0.00')

                # Select random products from different sellers
                available_products = random.sample(list(products), min(num_items, len(products)))

                for product in available_products:
                    quantity = Decimal(random.uniform(1, 10)).quantize(Decimal('0.1'))
                    
                    # Create order item
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price_per_unit=product.price_per_unit
                    )
                    
                    total_amount += quantity * product.price_per_unit

                # Update order total
                order.total_amount = total_amount + order.shipping_cost
                order.save()

                if (i + 1) % 10 == 0:
                    self.stdout.write(f'Created {i + 1} orders...')

            self.stdout.write(self.style.SUCCESS('Successfully created 100 test orders'))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating orders: {str(e)}')
            )