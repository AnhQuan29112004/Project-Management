from rest_framework import serializers
from Project.models import Project, Feedback, ResearchField
import os
import datetime

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
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['researchField'] = [
            rf.id for rf in instance.researchField.filter(is_deleted=0)
        ]
        representation['file'] = os.path.basename(instance.file.name) if instance.file else None
        return representation
    
    def create(self, validated_data):
        ts = datetime.datetime.now().timestamp()
        str_ts = str(ts).replace('.','_')
        file = validated_data.get('file')
        if file:
            file.name = f"{str_ts}_{file.name}"
        
        validated_data['file'] = file
        return super().create(validated_data)