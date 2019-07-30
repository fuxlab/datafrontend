from rest_framework import serializers

from annotations.models import AnnotationSegmentation


class AnnotationSegmentationSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = AnnotationSegmentation
        fields = ( 'id', 'image', 'category', 'category_name', 'mask', 'width', 'height' )

