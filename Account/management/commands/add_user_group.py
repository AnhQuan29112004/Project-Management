from Account.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from Project.models import Project, ResearchField
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.db import transaction

class Command(BaseCommand):
    help = "add user to group"
    
    def handle(self, *args, **options):
        all_users = CustomUser.objects.all()
        all_roles = CustomUser.RoleChoices.choices
        for i in all_users:
            if (i.role in [label for _,label in all_roles]):
                group = Group.objects.get(name=i.role)
                i.group.add(group)
                i.save()
                self.stdout.write(self.style.SUCCESS(f"User '{i.email}' added to group '{i.role}'."))