from rest_framework import serializers
from Project.models import Project, Feedback, ResearchField, ResearchFieldProject
import os
import datetime
from django.core.files.storage import FileSystemStorage
from pathlib import Path

class ResearchSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ResearchField
        fields = ['id','name','description','created_at','updated_at','updated_by','created_by']

class ProjectListSerializer(serializers.ModelSerializer):
    researchField = serializers.PrimaryKeyRelatedField(
        queryset=ResearchField.objects.filter(is_deleted=0), many=True, required=False
    )    
    file = serializers.ListField(
        child=serializers.FileField(), required=False, allow_empty=True
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
        file_upload = []
        if instance.file:
            for file in instance.file:
                file_upload.append(file)
        representation['file'] = file_upload
        return representation
    
    def create(self, validated_data):
        files = validated_data.pop('file', [])
        research_fields = validated_data.pop('researchField', [])
        file_upload = []
        file_storage = FileSystemStorage(location='media/projects/files')

        for file in files:
            ts = datetime.datetime.now().timestamp()
            str_ts = str(ts).replace('.','_')
            if file:
                file_storage.save(f"{str_ts}_{file.name}", file)
            file_upload.append(f"{str_ts}_{file.name}")
        validated_data['file'] = file_upload
        project = Project.objects.create(**validated_data)
        for field in research_fields:
            ResearchFieldProject.objects.create(
                project=project, researchField=field
            )
        return project
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        fileDelete = request.data.getlist('deletedFiles')
        files = validated_data.pop('file', [])
        research_fields = validated_data.pop('researchField', [])
        file_upload = []
        file_storage = FileSystemStorage(location='media/projects/files')
        breakpoint()
        if fileDelete:
            for file in fileDelete:
                path = Path(file_storage.path(file))
                if path.is_file():
                    file_storage.delete(file)
                    instance.file.remove(file)
        
        if files:
            for file in files:
                ts = datetime.datetime.now().timestamp()
                str_ts = str(ts).replace('.','_')
                if file:
                    file_storage.save(f"{str_ts}_{file.name}", file)
                file_upload.append(f"{str_ts}_{file.name}")
            validated_data['file'] = file_upload
        else:
            validated_data['file'] = instance.file
        all_fields = ResearchFieldProject.objects.all()
        for field in research_fields:
            if all_fields.filter(project=instance, researchField=field).exists():
                continue
            if field not in research_fields:
                ResearchFieldProject.objects.filter(
                    project=instance, researchField=field
                ).delete()
            ResearchFieldProject.objects.create(
                project=instance, researchField=field
            )
        
        return super().update(instance, validated_data)