from django.db.models.signals import post_save
from django.dispatch import receiver
from Account.models import CustomUser, UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        breakpoint()
        UserProfile.objects.create(user=instance)