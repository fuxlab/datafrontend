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
        if 'image_id' in filter_params:
            q = Annotation.objects.filter(image_id=filter_params['image_id'])
            queryset = queryset & q

        if 'category_id' in filter_params:
            q = Annotation.objects.filter(category_id=filter_params['category_id'])
            queryset = queryset & q
    
        return self.apply_range(queryset.order_by(self.get_sort()))
