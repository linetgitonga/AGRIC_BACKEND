from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Product, ProductImage
from crops.models import Crop
from faker import Faker
import random
from decimal import Decimal
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates 100 detailed farm products'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Expanded farm products data aligned with earlier crops
        products_data = [
            {
                'crop_name': 'tomato',
                'varieties': ['Roma', 'Cherry', 'Beefsteak', 'Plum', 'Heirloom', 'Grape'],
                'price_range': (50, 120),
                'quantity_range': (100, 1000),
                'units': ['kg', 'crate'],
                'descriptions': [
                    'Fresh, vine-ripened tomatoes perfect for salads and sauces',
                    'Organically grown tomatoes with rich flavor and firm texture',
                    'Premium greenhouse tomatoes grown using hydroponic techniques',
                    'Sun-ripened tomatoes harvested at peak freshness'
                ]
            },
            {
                'crop_name': 'potato',
                'varieties': ['Russet', 'Red', 'Yukon Gold', 'Fingerling', 'Purple', 'Sweet'],
                'price_range': (30, 80),
                'quantity_range': (500, 2000),
                'units': ['kg', 'bag', 'sack'],
                'descriptions': [
                    'Freshly harvested potatoes with excellent storage quality',
                    'Certified seed potatoes for planting next season',
                    'Washed and graded potatoes ready for market',
                    'Organic potatoes grown without synthetic pesticides'
                ]
            },
            {
                'crop_name': 'maize',
                'varieties': ['H614', 'H6213', 'H629', 'DK8031', 'PH4', 'PH7'],
                'price_range': (40, 70),
                'quantity_range': (1000, 5000),
                'units': ['kg', 'bag', 'ton'],
                'descriptions': [
                    'Grade 1 dry maize with less than 14% moisture content',
                    'High-yield hybrid maize suitable for animal feed',
                    'Non-GMO maize for flour production',
                    'Fresh green maize for roasting and boiling'
                ]
            },
            {
                'crop_name': 'banana',
                'varieties': ['Cavendish', 'Apple', 'Red', 'Plantain', 'Lady Finger'],
                'price_range': (20, 60),
                'quantity_range': (50, 500),
                'units': ['bunch', 'kg', 'finger'],
                'descriptions': [
                    'Tree-ripened bananas with perfect sweetness',
                    'Organic bananas grown without synthetic chemicals',
                    'Premium export-quality bananas',
                    'Freshly harvested green bananas for extended shelf life'
                ]
            },
            {
                'crop_name': 'cabbage',
                'varieties': ['Green', 'Red', 'Savoy', 'Napa', 'January King'],
                'price_range': (20, 50),
                'quantity_range': (100, 800),
                'units': ['head', 'kg'],
                'descriptions': [
                    'Fresh, tightly packed cabbage heads',
                    'Organic cabbage grown with natural fertilizers',
                    'Sweet and tender cabbage perfect for coleslaw',
                    'Disease-resistant cabbage varieties'
                ]
            },
            {
                'crop_name': 'onion',
                'varieties': ['Red', 'White', 'Yellow', 'Shallot', 'Spring'],
                'price_range': (30, 70),
                'quantity_range': (200, 1500),
                'units': ['kg', 'bag', 'bulb'],
                'descriptions': [
                    'Well-cured onions with excellent storage quality',
                    'Sweet onions perfect for salads',
                    'Large-sized onions for commercial kitchens',
                    'Organic onions grown with natural pest control'
                ]
            },
            {
                'crop_name': 'carrot',
                'varieties': ['Nantes', 'Chantenay', 'Imperator', 'Baby', 'Purple'],
                'price_range': (40, 90),
                'quantity_range': (100, 800),
                'units': ['kg', 'bunch'],
                'descriptions': [
                    'Sweet and crunchy carrots with deep orange color',
                    'Organic carrots rich in beta-carotene',
                    'Baby carrots perfect for snacks and lunchboxes',
                    'Freshly harvested carrots with tops attached'
                ]
            },
            {
                'crop_name': 'rice',
                'varieties': ['Basmati', 'Jasmine', 'Arborio', 'Brown', 'Red'],
                'price_range': (80, 150),
                'quantity_range': (500, 3000),
                'units': ['kg', 'bag', 'sack'],
                'descriptions': [
                    'Premium quality rice with low breakage percentage',
                    'Organic paddy rice for health-conscious consumers',
                    'Aromatic rice varieties for special dishes',
                    'Newly harvested rice with excellent cooking quality'
                ]
            },
            {
                'crop_name': 'wheat',
                'varieties': ['Hard Red', 'Soft White', 'Durum', 'Einkorn', 'Emmer'],
                'price_range': (50, 100),
                'quantity_range': (1000, 5000),
                'units': ['kg', 'bag', 'ton'],
                'descriptions': [
                    'High-protein wheat for bread making',
                    'Organic wheat for health-conscious bakers',
                    'Clean, well-stored wheat with low moisture',
                    'Premium quality wheat for commercial flour mills'
                ]
            },
            {
                'crop_name': 'mango',
                'varieties': ['Apple', 'Kent', 'Tommy Atkins', 'Ngowe', 'Keitt'],
                'price_range': (30, 80),
                'quantity_range': (50, 400),
                'units': ['piece', 'kg', 'crate'],
                'descriptions': [
                    'Tree-ripened mangoes with perfect sweetness',
                    'Export-quality mangoes with uniform size',
                    'Organic mangoes grown without synthetic pesticides',
                    'Freshly harvested mature green mangoes for extended shelf life'
                ]
            }
        ]

        # Get some seller users (farmers)
        sellers = User.objects.filter(user_type='farmer')
        if not sellers:
            self.stdout.write(self.style.ERROR('No farmer users found. Please create some farmers first.'))
            return

        # Kenya locations with more variety
        locations = [
            {'name': 'Nakuru', 'lat': -0.3031, 'lon': 36.0800},
            {'name': 'Nyeri', 'lat': -0.4169, 'lon': 36.9514},
            {'name': 'Meru', 'lat': 0.0500, 'lon': 37.6500},
            {'name': 'Kisumu', 'lat': -0.1000, 'lon': 34.7500},
            {'name': 'Eldoret', 'lat': 0.5167, 'lon': 35.2833},
            {'name': 'Kitale', 'lat': 1.0167, 'lon': 35.0000},
            {'name': 'Thika', 'lat': -1.0333, 'lon': 37.0833},
            {'name': 'Kericho', 'lat': -0.3667, 'lon': 35.2833},
            {'name': 'Embu', 'lat': -0.5333, 'lon': 37.4500},
            {'name': 'Machakos', 'lat': -1.5167, 'lon': 37.2667},
        ]

        try:
            for i in range(100):  # Create 100 products
                # Random product data
                product_type = random.choice(products_data)
                location = random.choice(locations)
                seller = random.choice(sellers)
                
                # Get or create crop
                crop, _ = Crop.objects.get_or_create(
                    name=product_type['crop_name'],
                    defaults={'description': f"Standard {product_type['crop_name']} crop"}
                )

                # Generate dates with more variety
                harvest_date = datetime.now() - timedelta(days=random.randint(1, 60))
                expiry_date = harvest_date + timedelta(days=random.randint(7, 180))

                # Create product with more detailed attributes
                product = Product.objects.create(
                    seller=seller,
                    crop=crop,
                    title=f"{random.choice(product_type['varieties'])} {product_type['crop_name'].title()}",
                    description=random.choice(product_type['descriptions']),
                    price_per_unit=Decimal(random.uniform(
                        product_type['price_range'][0],
                        product_type['price_range'][1]
                    )).quantize(Decimal('0.01')),
                    unit=random.choice(product_type['units']),
                    quantity_available=Decimal(random.uniform(
                        product_type['quantity_range'][0],
                        product_type['quantity_range'][1]
                    )).quantize(Decimal('0.01')),
                    harvest_date=harvest_date.date(),
                    expiry_date=expiry_date.date(),
                    is_organic=random.choice([True, False, False, False]),  # 25% organic
                    is_featured=random.choice([True, False, False]),  # 33% featured
                    status=random.choice(['available', 'available', 'available', 'limited']),
                    location=location['name'],
                    latitude=location['lat'],
                    longitude=location['lon'],
                    min_order_quantity=Decimal(random.choice([1, 5, 10, 20])),
                    packaging=random.choice(['plastic', 'mesh', 'carton', 'none']),
                    certification=random.choice(['None', 'Organic', 'GAP', 'Fairtrade', 'None']),
                    delivery_available=random.choice([True, False])
                )

                # Create 1-3 product images
                for img_num in range(random.randint(1, 3)):
                    ProductImage.objects.create(
                        product=product,
                        image=f"products/{product_type['crop_name']}_{img_num}.jpg",
                        is_primary=(img_num == 0)
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created product: {product.title} - {product.quantity_available}{product.unit} at KSh{product.price_per_unit}/{product.unit} ({product.location})'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating products: {str(e)}')
            )