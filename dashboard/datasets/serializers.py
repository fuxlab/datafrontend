from rest_framework import serializers

from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dataset
        fields = ( 'id', 'project', 'identifier', 'name', 'images_count', 'version', 'description', 'contributor', 'url', 'release_date')
