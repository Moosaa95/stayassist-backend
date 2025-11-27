from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile when a new CustomUser is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the profile whenever the user is saved.
    """
    if hasattr(instance, "profile"):
        instance.profile.save()
