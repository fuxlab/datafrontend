from rest_framework import serializers

from annotations.models import AnnotationBoundingbox


class AnnotationBoundingboxSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = AnnotationBoundingbox
        fields = ( 'id', 'image', 'category', 'category_name', 'x_min', 'x_max', 'y_min', 'y_max' )
