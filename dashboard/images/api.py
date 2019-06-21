from rest_framework import permissions
from dashboard.lib.api_base import DashboardApiBase
from .models import Image
from .serializers import ImageSerializer

class ImageViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ImageSerializer


    def get_queryset(self):
        '''
        define queryset
        '''
        queryset = Image.objects.all()
        
        filter_params = self.get_filter()
        if 'dataset' in filter_params:
            q = Image.objects.filter(dataset=filter_params['dataset'])
            queryset = queryset & q

        if 'category' in filter_params:
            q = Image.objects.filter(annotation__category=filter_params['category'])
            queryset = queryset & q

        if 'q' in filter_params:
            q1 = Image.objects.filter(name__contains=filter_params['q'])
            q2 = Image.objects.filter(url__contains=filter_params['q'])
            queryset = queryset & (q1 | q2)
    
        return queryset.order_by(self.get_sort())

