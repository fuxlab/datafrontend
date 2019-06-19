from rest_framework import viewsets, permissions
from dashboard.lib.api_base import DashboardApiBase

from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(DashboardApiBase):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategorySerializer


    def get_queryset(self):
        '''
        define queryset
        '''
        queryset = Category.objects.all()
        
        filter_params = self.get_filter()
        if 'dataset' in filter_params:
            q = Category.objects.filter(dataset=filter_params['dataset'])
            queryset = queryset & q

        if 'q' in filter_params:
            q1 = Category.objects.filter(name__contains=filter_params['q'])
            queryset = queryset & (q1)
    
        return self.apply_range(queryset.order_by(self.get_sort()))
