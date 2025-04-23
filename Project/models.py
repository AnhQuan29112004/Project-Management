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
    
    
class Feedback(models.Model):
    feedback = models.TextField(max_length=200)
    feedbacker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacker')


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    researchField = models.ManyToManyField(ResearchField,through='ResearchFieldProject')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='updated_projects')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='projects')
    feedback = models.ForeignKey(Feedback,on_delete=models.CASCADE, related_name="projectfeedback",null=True, blank=True)
    feedBackText = models.TextField(null=True, blank=True, default=None)
    feedBack_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbackByProject',default=None)
    file = models.JSONField(null=True, blank=True, default=dict)  
    def __str__(self):
        return self.name 
    
class ResearchFieldProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name="projectresearchfield")
    researchField = models.ForeignKey(ResearchField,on_delete=models.CASCADE,related_name="researchproject")
    