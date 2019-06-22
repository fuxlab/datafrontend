from rest_framework import serializers

from .models import Annotation, AnnotationBoundingbox, AnnotationSegmentation


class AnnotationSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Annotation
        fields = ( 'id', 'image', 'category', 'category_name', 'types', 'image_name' )



class AnnotationBoundingboxSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = AnnotationBoundingbox
        fields = ( 'id', 'image', 'category', 'category_name', 'x_min', 'x_max', 'y_min', 'y_max' )



class AnnotationSegmentationSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = AnnotationSegmentation
        fields = ( 'id', 'image', 'category', 'category_name', 'mask', 'width', 'height' )

