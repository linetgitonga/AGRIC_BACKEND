# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import FarmerProfile, BuyerProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'farmer':
            FarmerProfile.objects.create(user=instance)
        elif instance.user_type == 'buyer':
            BuyerProfile.objects.create(user=instance)