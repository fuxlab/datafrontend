from rest_framework import permissions
from dashboard.lib.api_base import DashboardApiBase
from .models import Annotation
from .serializers import AnnotationSerializer

class AnnotationViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnotationSerializer


    def get_queryset(self):
        '''
        define queryset
        '''
        queryset = Annotation.objects.all()
        
        filter_params = self.get_filter()

        if 'image' in filter_params:
            q = Annotation.objects.filter(image=filter_params['image'])
            queryset = queryset & q

        if 'category' in filter_params:
            q = Annotation.objects.filter(category=filter_params['category'])
            queryset = queryset & q

        if 'dataset' in filter_params:
            q = Annotation.objects.filter(image__dataset_id=filter_params['dataset'])
            queryset = queryset & q


        if 'type' in filter_params:
            filter_types = filter_params['type'].split(',')
            for filter_type in filter_types:
                #if filter_type == 'annotation':
                #    # q = Annotation.objects.filter(category_id=filter_params['category_id'])
                #    # queryset = queryset & q
                if filter_type == 'boundingbox':
                    q = Annotation.objects.exclude(annotationboundingbox=None)
                    queryset = queryset & q
                elif filter_type == 'segmentation':
                    q = Annotation.objects.exclude(annotationsegmentation=None)
                    queryset = queryset & q

    
        return self.apply_range(queryset.order_by(self.get_sort()))
