from rest_framework import serializers

from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ( 'id', 'project', 'name', 'annotations_count', 'boundingboxes_count', 'segmentations_count')
