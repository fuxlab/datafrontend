# Create your views here.
from rest_framework import viewsets, permissions
from dashboard.lib.api_base import DashboardApiBase
from dashboard.lib.pagination import Pagination

from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(DashboardApiBase):
    permission_classes = [
        permissions.AllowAny
    ]
    
    serializer_class = ProjectSerializer

    def get_queryset(self):
        '''
        define queryset
        '''
        queryset = Project.objects.all()
        
        filter_params = self.get_filter()

        if 'q' in filter_params:
            q1 = Project.objects.filter(name__contains=filter_params['q'])
            queryset = queryset & q1
    
        return queryset.order_by(self.get_sort())