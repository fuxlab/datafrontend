from rest_framework import serializers

from .models import Annotation

class AnnotationSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Annotation
        fields = ( 'id', 'image', 'category', 'types', 'image_preview' )
