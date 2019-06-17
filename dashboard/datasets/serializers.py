from rest_framework import serializers

from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dataset
        fields = ( 'id', 'project_id', 'identifier', 'name', )
