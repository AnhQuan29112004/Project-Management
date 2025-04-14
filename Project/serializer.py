from rest_framework import serializers
from Project.models import Project, Feedback, ResearchField

class ResearchSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = ResearchField
        fields = ['name','description']

class ProjectListSerializer(serializers.ModelSerializer):
    research_field = serializers.PrimaryKeyRelatedField(
        queryset=ResearchField.objects.all(), many=True, required=False
    )    
    class Meta:
        model = Project
        fields = ['name','description','start_date','end_date','summary','file','research_field']