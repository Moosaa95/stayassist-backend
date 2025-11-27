from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from stay.models import Listing
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding listings...')

        # Create a host user if one doesn't exist
        host_email = 'host@example.com'
        host, created = User.objects.get_or_create(
            email=host_email,
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'is_active': True,
            }
        )
        if created:
            host.set_password('password123')
            host.save()
            self.stdout.write(self.style.SUCCESS(f'Created host user: {host_email}'))
        else:
            self.stdout.write(f'Using existing host user: {host_email}')

        # Sample listings data
        listings_data = [
            {
                'title': 'Luxury Beachfront Villa',
                'description': 'Beautiful 3-bedroom villa with stunning ocean views, private pool, and direct beach access. Perfect for families or groups looking for a relaxing getaway.',
                'price_per_night': Decimal('250.00'),
                'city': 'Miami',
                'photos': [
                    'https://images.unsplash.com/photo-1512917774080-9991f1c4c750',
                    'https://images.unsplash.com/photo-1613490493576-7fde63acd811',
                ],
                'host': host,
            },
            {
                'title': 'Downtown Modern Loft',
                'description': 'Stylish loft in the heart of the city with contemporary design, high ceilings, and all modern amenities. Walking distance to restaurants and entertainment.',
                'price_per_night': Decimal('180.00'),
                'city': 'New York',
                'photos': [
                    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688',
                    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2',
                ],
                'host': host,
            },
            {
                'title': 'Cozy Mountain Cabin',
                'description': 'Charming 2-bedroom cabin nestled in the mountains. Features fireplace, hot tub, and breathtaking views. Ideal for nature lovers and winter sports enthusiasts.',
                'price_per_night': Decimal('150.00'),
                'city': 'Denver',
                'photos': [
                    'https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8',
                    'https://images.unsplash.com/photo-1518780664697-55e3ad937233',
                ],
                'host': host,
            },
            {
                'title': 'Seaside Cottage',
                'description': 'Quaint cottage with ocean views and private garden. Perfect for couples seeking a romantic retreat by the sea.',
                'price_per_night': Decimal('120.00'),
                'city': 'San Diego',
                'photos': [
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791',
                    'https://images.unsplash.com/photo-1566073771259-6a8506099945',
                ],
                'host': host,
            },
            {
                'title': 'Urban Penthouse Suite',
                'description': 'Luxury penthouse with panoramic city views, rooftop terrace, and premium furnishings. Experience city living at its finest.',
                'price_per_night': Decimal('320.00'),
                'city': 'Chicago',
                'photos': [
                    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267',
                    'https://images.unsplash.com/photo-1567767292278-a4f21aa2d36e',
                ],
                'host': host,
            },
            {
                'title': 'Historic Victorian Home',
                'description': 'Beautifully restored Victorian house with period details, modern comforts, and elegant garden. A unique blend of history and luxury.',
                'price_per_night': Decimal('200.00'),
                'city': 'San Francisco',
                'photos': [
                    'https://images.unsplash.com/photo-1568605114967-8130f3a36994',
                    'https://images.unsplash.com/photo-1570129477492-45c003edd2be',
                ],
                'host': host,
            },
            {
                'title': 'Lakefront Retreat',
                'description': 'Peaceful 4-bedroom home on a private lake with dock, kayaks, and fire pit. Perfect for family vacations and water activities.',
                'price_per_night': Decimal('190.00'),
                'city': 'Austin',
                'photos': [
                    'https://images.unsplash.com/photo-1544984243-ec57ea16fe25',
                    'https://images.unsplash.com/photo-1559827260-dc66d52bef19',
                ],
                'host': host,
            },
            {
                'title': 'Desert Oasis Villa',
                'description': 'Stunning modern villa with pool, outdoor entertainment area, and mountain views. Experience luxury in the desert.',
                'price_per_night': Decimal('280.00'),
                'city': 'Phoenix',
                'photos': [
                    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9',
                    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c',
                ],
                'host': host,
            },
        ]

        # Create listings
        created_count = 0
        for listing_data in listings_data:
            listing, created = Listing.objects.get_or_create(
                title=listing_data['title'],
                defaults=listing_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created listing: {listing.title}')
                )
            else:
                self.stdout.write(f'Listing already exists: {listing.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeding complete! Created {created_count} new listings.'
            )
        )
