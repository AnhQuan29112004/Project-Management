from django.db import models
from Account.models import CustomUser

# Create your models here.
class ResearchField(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_research_fields')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='created_research_fields')
    def __str__(self):
        return self.name
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    research_field = models.ManyToManyField(ResearchField)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_projects')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='projects')
    file = models.FileField(upload_to='projects/files/', null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    feedbacker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacker')
    def __str__(self):
        return self.name
    