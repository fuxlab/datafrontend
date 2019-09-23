import os

from rest_framework import viewsets, permissions
from dashboard.lib.api_base import DashboardApiBase
from django.db.models import Q

from datasets.models import Dataset
from datasets.serializers import DatasetSerializer

from datasets.tasks.init_folder import init_folder_task

from django.conf import settings

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

        if 'category' in filter_params:
            qs.add((
                Q(image__annotation__category=filter_params['category']) |
                Q(image__annotationboundingbox__category=filter_params['category']) |
                Q(image__annotationsegmentation__category=filter_params['category'])
            ), Q.AND)

        if 'q' in filter_params:
            qs.add(Q(name__contains=filter_params['q']) | Q(identifier__contains=filter_params['q']), Q.AND)
    
        return Dataset.objects.filter(qs).distinct().order_by(self.get_sort())


    def perform_create(self, serializer):
        '''
        create new dataset, create folder and create task
        '''
        serializer.save()
        
        path = os.path.join(settings.DATAFRONTEND['DATA_PATH'], serializer.validated_data['identifier'])
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        else:
            # todo write queue
            init_folder_task(serializer.data['id'])
        
