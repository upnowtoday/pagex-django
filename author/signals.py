from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def profile_connect(instance, created, **kwargs):
    if created:  # action when a new user created on DB
        Profile.objects.create(user=instance)
