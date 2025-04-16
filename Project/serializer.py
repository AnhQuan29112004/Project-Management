from rest_framework import serializers
from Project.models import Project, Feedback, ResearchField

class ResearchSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = ResearchField
        fields = ['id','name','description','created_at','updated_at','updated_by','created_by']

class ProjectListSerializer(serializers.ModelSerializer):
    researchField = serializers.PrimaryKeyRelatedField(
        queryset=ResearchField.objects.filter(is_deleted=0), many=True, required=False
    )    
    class Meta:
        model = Project
        fields = ['id','name','description','start_date','end_date','summary','file','researchField','created_at','updated_at','updated_by','created_by']
    
    def validate(self, attrs):
        if attrs.get('start_date') and attrs.get('end_date'):
            if attrs['start_date'] > attrs['end_date']:
                raise serializers.ValidationError("Start date must be before end date.")
        return super().validate(attrs)