from rest_framework import viewsets, permissions
from dashboard.lib.api_base import DashboardApiBase

from .models import Dataset
from .serializers import DatasetSerializer

class DatasetViewSet(DashboardApiBase):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DatasetSerializer


    def get_queryset(self):
        '''
        define queryset
        '''
        queryset = Dataset.objects.all()
        
        filter_params = self.get_filter()
        if 'project_id' in filter_params:
            q = Dataset.objects.filter(project_id=filter_params['project_id'])
            queryset = queryset & q

        if 'q' in filter_params:
            q1 = Dataset.objects.filter(name__contains=filter_params['q'])
            q2 = Dataset.objects.filter(identifier__contains=filter_params['q'])
            queryset = queryset & (q1 | q2)
    
        return self.apply_range(queryset.order_by(self.get_sort()))
