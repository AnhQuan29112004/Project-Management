from Account.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from Project.models import Project, ResearchField, Feedback
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.db import transaction

class Command(BaseCommand):
    help = "Create Permissions"
    
    def handle(self, *args, **options):
        content_type_project = ContentType.objects.get_for_model(Project)
        view_project = Permission.objects.get(codename='view_project', content_type=content_type_project)
        add_project = Permission.objects.get(codename='add_project', content_type=content_type_project)
        change_project = Permission.objects.get(codename='change_project', content_type=content_type_project)
        delete_project = Permission.objects.get(codename='delete_project', content_type=content_type_project)
        delete_project = Permission.objects.get(codename='delete_project', content_type=content_type_project)

        delete_project = Permission.objects.get(codename='delete_project', content_type=content_type_project)

        content_type_research_field = ContentType.objects.get_for_model(ResearchField)
        view_research_field_perm = Permission.objects.get(codename='view_researchfield', content_type=content_type_research_field)
        
        
        student_group = Group.objects.get(name='Student')
        student_group.permissions.set([view_project])

        lecturer_group = Group.objects.get(name='Lecturer')
        lecturer_group.permissions.set([
            view_project,
            add_project,
            change_project,
            delete_project,
            view_research_field_perm
        ])

        admin_group = Group.objects.get(name='Admin')
        admin_group.permissions.set(Permission.objects.all())