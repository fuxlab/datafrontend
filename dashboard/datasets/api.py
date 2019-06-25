from rest_framework import viewsets, permissions
from dashboard.lib.api_base import DashboardApiBase
from django.db.models import Q

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
        qs = Q()
        
        filter_params = self.get_filter()
        if 'project' in filter_params:
            qs.add(Q(project=filter_params['project']), Q.AND)

        if 'q' in filter_params:
            qs.add(Q(name__contains=filter_params['q']) | Q(identifier__contains=filter_params['q']), Q.AND)
    
        return Dataset.objects.filter(qs).distinct().order_by(self.get_sort())
