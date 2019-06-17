# Create your views here.
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
        if 'dataset_id' in filter_params:
            q = Image.objects.filter(dataset_id=filter_params['dataset_id'])
            queryset = queryset & q

        if 'q' in filter_params:
            q1 = Image.objects.filter(name__contains=filter_params['q'])
            q2 = Image.objects.filter(url__contains=filter_params['q'])
            queryset = queryset & (q1 | q2)
    
        return self.apply_range(queryset.order_by(self.get_sort()))
