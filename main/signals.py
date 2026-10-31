from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
import random





@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        last_profile = UserProfile.objects.order_by('-id').first()
        next_number = 1

        if last_profile and last_profile.code:
            last_code = int(last_profile.code[1:])
            next_number = last_code + 1

        if next_number > 50:
            code = 'MAX'  # Or raise error
        else:
            code = f"A{next_number}"

