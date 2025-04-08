from Account.models import CustomUser
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db import transaction

class Command(BaseCommand):
    help = "Create Groups"
    
    def handle(self, *args, **options):
        roles = CustomUser.RoleChoices.choices
        
        for role_value, role_label in roles:
            group, created = Group.objects.get_or_create(name=role_label)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Group '{role_label}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"Group '{role_label}' already exists."))
        