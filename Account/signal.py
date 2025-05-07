from django.db.models.signals import post_save
from django.dispatch import receiver
from Account.models import CustomUser, UserProfile
from Account.management.commands import add_user_group, create_perm

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        add_user_group.Command().handle()