from rest_framework import serializers

from images.models import Image

class ExportSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        '''
        super init and accept filter_params
        '''
        self.filter_params = kwargs.get('filter_params', {} )
        kwargs.pop('filter_params', None)
        super(ExportSerializer, self).__init__(*args, **kwargs)

    def queryset_fields(filter_params):
        '''
        mapping for query resultset
        '''
        fields = [ 'id' ]
        if 'category' in filter_params:
            filter_type = filter_params['type'] if 'type' in filter_params else 'all'

            if filter_type == 'all':
                fields.append('annotation__id')
                fields.append('annotation__category_id')
            
            if filter_type == 'boundingbox':
                fields.append('annotationboundingbox__id')
                fields.append('annotationboundingbox__category_id')
                fields.append('annotationboundingbox__x_min')
                fields.append('annotationboundingbox__x_max')
                fields.append('annotationboundingbox__y_min')
                fields.append('annotationboundingbox__y_max')
            
            if filter_type == 'segmentation':
                fields.append('annotationsegmentation__id')
                fields.append('annotationsegmentation__category_id')
                fields.append('annotationsegmentation__mask')
            
            if filter_type == 'annotation':
                fields.append('annotation__id')
                fields.append('annotation__category_id')
        else:
            fields.append('dataset_id')

        return fields

    def get_url(self, obj):
        '''
        return path of relevant image
        '''
        if 'category' in self.filter_params:
            if 'annotationboundingbox__id' in obj and obj['annotationboundingbox__id'] is not None:
                return '/api/image/boundingbox_crop/%s.png' % (obj['annotationboundingbox__id'])
            elif 'annotationsegmentation__id' in obj and obj['annotationsegmentation__id'] is not None:
                return '/api/image/segmentation_crop/%s.png' % (obj['annotationsegmentation__id'])
            else:
                return '/api/image/%s.png' % (obj['id'])

        return '/api/image/%s.png' % (obj['id'])


    def get_id(self, obj):
        '''
        get an unique id to display. due to we have multiple models, and potentially overlapping ids
        we need to calculate a new unique one
        '''
        id_parts = [ str(obj['id']) ]
        if 'category' in self.filter_params:
            if 'annotation__id' in obj and obj['annotation__id'] is not None:
                id_parts.append(str(obj['annotation__id']))
            if 'annotationboundingbox__id' in obj and obj['annotationboundingbox__id'] is not None:
                id_parts.append(str(obj['annotationboundingbox__id']))
            if 'annotationsegmentation__id' in obj and obj['annotationsegmentation__id'] is not None:
                id_parts.append(str(obj['annotationsegmentation__id']))

        return str('-'.join(id_parts))


    def get_type(self, obj):
        '''
        get type of record by filter_params and returning record data
        '''
        if 'category' in self.filter_params:
            queryset_fields = ExportSerializer.queryset_fields(self.filter_params)
            if 'annotationboundingbox__id' in obj and obj['annotationboundingbox__id'] is not None:
                return 'boundingbox'
            elif 'annotationsegmentation__id' in obj and  obj['annotationsegmentation__id'] is not None:
                return 'segmentation'
            else:
                return 'annotation'
        
        return 'image'


    def get_image(self, obj):
        '''
        get original image source path
        '''
        return '/api/image/%s.png' % (obj['id'])


    def get_category(self, obj):
        '''
        get class for type
        '''
        if 'category' in self.filter_params:
            if 'annotation__category_id' in obj and obj['annotation__category_id'] is not None:
                return obj['annotation__category_id']
            if 'annotationboundingbox__category_id' in obj and obj['annotationboundingbox__category_id'] is not None:
                return obj['annotationboundingbox__category_id']
            if 'annotationsegmentation__category_id' in obj and obj['annotationsegmentation__category_id'] is not None:
                return obj['annotationsegmentation__category_id']
        elif 'dataset_id' in obj and obj['dataset_id'] is not None:                
            return obj['dataset_id']
        return 0
        
    class Meta:
        '''
        data returned with json-api
        '''
        model = Image
        fields = [ 'id', 'type', 'url', 'image', 'category' ]