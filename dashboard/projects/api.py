# Create your views here.
from rest_framework import viewsets, permissions
from dashboard.lib.api_base import DashboardApiBase
from dashboard.lib.pagination import Pagination
from django.db.models import Q

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
        qs = Q()     
        filter_params = self.get_filter()

        if 'q' in filter_params:
            qs.add(Q(name__contains=filter_params['q']), Q.AND)
    
        return Project.objects.filter(qs).distinct().order_by(self.get_sort())
