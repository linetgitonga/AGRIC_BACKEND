from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Product, Review
from faker import Faker
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates 500 product reviews'

    def handle(self, *args, **options):
        fake = Faker()

        # Get available products and users
        products = list(Product.objects.all())
        users = list(User.objects.all())

        if not products:
            self.stdout.write(self.style.ERROR('No products found. Please create products first.'))
            return

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create users first.'))
            return

        # Review templates for different ratings
        review_templates = {
            5: [
                "Excellent quality {product}! Exceeded my expectations. {detail}",
                "Best {product} I've ever bought. {detail}",
                "Outstanding freshness and quality. {detail}",
                "Highly recommend this seller's {product}. {detail}"
            ],
            4: [
                "Very good {product}, satisfied with the purchase. {detail}",
                "Good quality and fair price for {product}. {detail}",
                "Nice product, would buy again. {detail}",
                "Better than expected {product}. {detail}"
            ],
            3: [
                "Average quality {product}, acceptable. {detail}",
                "Decent {product} for the price. {detail}",
                "Not bad, but could be better. {detail}",
                "Reasonable quality {product}. {detail}"
            ],
            2: [
                "Below average {product}. {detail}",
                "Not very satisfied with this {product}. {detail}",
                "Expected better quality. {detail}",
                "Might need improvements. {detail}"
            ],
            1: [
                "Disappointed with this {product}. {detail}",
                "Poor quality product. {detail}",
                "Would not recommend. {detail}",
                "Not worth the price. {detail}"
            ]
        }

        positive_details = [
            "Fresh and well-packaged.",
            "Arrived in perfect condition.",
            "Great communication from seller.",
            "Fast delivery and professional service.",
            "Very satisfied with the quality.",
            "Will definitely order again.",
            "Excellent value for money.",
            "Perfectly ripened and ready to use."
        ]

        negative_details = [
            "Delivery could be improved.",
            "Packaging needs improvement.",
            "Communication was lacking.",
            "Size/quantity was less than expected.",
            "Some items were damaged.",
            "Took longer than expected to arrive.",
            "Price is a bit high for the quality.",
            "Not as fresh as expected."
        ]

        self.stdout.write('Creating reviews...')
        reviews_created = 0
        attempts = 0
        max_attempts = 1000  # Prevent infinite loop

        try:
            while reviews_created < 500 and attempts < max_attempts:
                attempts += 1
                user = random.choice(users)
                product = random.choice(products)

                # Skip if user already reviewed this product
                if Review.objects.filter(user=user, product=product).exists():
                    continue

                # Generate rating with weighted probability
                rating = random.choices(
                    [5, 4, 3, 2, 1],
                    weights=[0.4, 0.3, 0.15, 0.1, 0.05]
                )[0]

                # Select review template and detail
                template = random.choice(review_templates[rating])
                detail = random.choice(positive_details if rating > 3 else negative_details)

                # Generate review text
                comment = template.format(
                    product=product.title.lower(),
                    detail=detail
                )

                # Create review with a random past date
                review = Review.objects.create(
                    product=product,
                    user=user,
                    rating=rating,
                    comment=comment,
                    created_at=datetime.now() - timedelta(
                        days=random.randint(0, 60),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                )

                reviews_created += 1
                if reviews_created % 50 == 0:
                    self.stdout.write(f'Created {reviews_created} reviews...')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {reviews_created} reviews'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating reviews: {str(e)}')
            )