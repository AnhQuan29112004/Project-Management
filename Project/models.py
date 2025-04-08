from django.db import models
from Account.models import CustomUser

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='projects/files/', null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    feedbacker = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacker')
    def __str__(self):
        return self.name