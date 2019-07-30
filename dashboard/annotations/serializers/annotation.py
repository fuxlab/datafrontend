from rest_framework import serializers

from annotations.models import Annotation


class AnnotationSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Annotation
        fields = ( 'id', 'image', 'category', 'category_name', 'image_name' )
