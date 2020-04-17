from rest_framework import serializers

from annotations.models import Annotation


class AnnotationBoundingboxSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Annotation
        fields = (
            'id',
            'image',
            'category',
            'category_name',
            'image_name',
            
            'x_min',
            'x_max',
            'y_min',
            'y_max',

            'area',
            'width',
            'height'
        )
