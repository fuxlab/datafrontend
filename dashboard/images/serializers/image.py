from rest_framework import serializers

from images.models import Image

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Image
        fields = ( 'id', 'dataset', 'name', 'url', 'types', 'path', 'image', 'preview', 'thumbnail' )
