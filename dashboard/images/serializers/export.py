from rest_framework import serializers

from images.models import Image

class ExportSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()

    annotation_image = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()


    def __init__(self, *args, **kwargs):
        '''
        super init and accept export_params
        '''
        self.export_params = kwargs.get('export_params', {} )
        kwargs.pop('export_params', None)
        super(ExportSerializer, self).__init__(*args, **kwargs)


    def get_id(self, obj):
        '''
        '''
        return obj.id


    def get_type(self, obj):
        '''
        get type of record by export_params
        '''
        if 'type' in self.export_params:
            return self.export_params['type']
        
        return 'all'


    def get_annotation_image(self, obj):
        '''
        get preview image source path
        '''
        if 'type' in self.export_params and self.export_params['type'] not in [ 'annotation' ]:
            return '/api/image/%s_%s.png' % (self.export_params['type'], obj.id)
        return '/api/image/%s.png' % (obj.id)


    def get_image(selg, obj):
        '''
        '''
        return obj.image.image()


    def get_source(self, obj):
        '''
        get class for type
        '''
        sstr = []
        if 'category' in self.export_params:
            sstr.append(obj.category.name)
        if 'dataset' in self.export_params:
            sstr.append(obj.image.dataset.name)
        return ' '.join(sstr) 

        
    class Meta:
        '''
        data returned with json-api
        '''
        model = Image
        fields = [ 'id', 'type', 'annotation_image', 'image', 'source' ] #, 'url'

