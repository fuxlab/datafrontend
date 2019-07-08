from rest_framework import serializers

from images.models import Image

class ExportSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()


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
        if 'category' in filter_params:
            return [
                'id',
                'annotation__id',
                'annotationboundingbox__id',
                'annotationsegmentation__id',
                'annotation__category_id',
                'annotationboundingbox__category_id',
                'annotationsegmentation__category_id',
                
                'annotationboundingbox__x_min',
                'annotationboundingbox__x_max',
                'annotationboundingbox__y_min',
                'annotationboundingbox__y_max',

                'annotationsegmentation__mask',
            ]
        else:
            return [
                'id',
                'dataset_id' 
            ]


    def get_url(self, obj):
        '''
        return path of relevant image
        '''
        queryset_fields = ExportSerializer.queryset_fields(self.filter_params)
        
        if 'category' in self.filter_params:
            if obj[queryset_fields.index('annotationboundingbox__id')] is not None:
                return '/api/image/boundingbox_crop/%s.png' % (obj[queryset_fields.index('annotationboundingbox__id')])
            elif obj[queryset_fields.index('annotationsegmentation__id')] is not None:
                return '/api/image/segmentation_crop/%s.png' % (obj[queryset_fields.index('annotationsegmentation__id')])
            else:
                return '/api/image/%s.png' % (obj[queryset_fields.index('id')])

        return '/api/image/%s.png' % (obj[queryset_fields.index('id')])


    def get_id(self, obj):
        '''
        get an unique id to display. due to we have multiple models, and potentially overlapping ids
        we need to calculate a new unique one
        '''
        queryset_fields = ExportSerializer.queryset_fields(self.filter_params)
        if 'category' in self.filter_params:
            if obj[queryset_fields.index('annotationboundingbox__id')] is not None:
                return '%s-%s' % (obj[queryset_fields.index('id')], obj[queryset_fields.index('annotationboundingbox__id')])
            elif obj[queryset_fields.index('annotationsegmentation__id')] is not None:
                return '%s-%s' % (obj[queryset_fields.index('id')], obj[queryset_fields.index('annotationsegmentation__id')])
            else:
                return '%s-%s' % (obj[queryset_fields.index('id')], obj[queryset_fields.index('annotation__id')])
        
        return obj[queryset_fields.index('id')]


    def get_type(self, obj):
        '''
        get type of record by filter_params and returning record data
        '''
        if 'category' in self.filter_params:
            queryset_fields = ExportSerializer.queryset_fields(self.filter_params)
            if obj[queryset_fields.index('annotationboundingbox__id')] is not None:
                return 'boundingbox'
            elif obj[queryset_fields.index('annotationsegmentation__id')] is not None:
                return 'segmentation'
            else:
                return 'annotation'
        
        return 'image'


    class Meta:
        '''
        data returned with json-api
        '''
        model = Image
        fields = [ 'id', 'type', 'url' ]
