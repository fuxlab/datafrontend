from rest_framework import viewsets, permissions
from dashboard.lib.api_base import DashboardApiBase
from django.db.models import Q

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
        qs = Q()
        filter_params = self.get_filter()

        if 'project' in filter_params:
            qs.add(Q(project=filter_params['project']), Q.AND)

        if 'q' in filter_params:
            qs.add(Q(name__contains=filter_params['q']), Q.AND)

        if 'dataset_annotation' in filter_params:
            qs.add((
                Q(annotation__image__dataset_id=filter_params['dataset_annotation'])
            ), Q.AND)

        if 'dataset_boundingbox' in filter_params:
            qs.add((
                Q(annotationboundingbox__image__dataset_id=filter_params['dataset_boundingbox'])
            ), Q.AND)

        if 'dataset_segmentation' in filter_params:
            qs.add((
                Q(annotationsegmentation__image__dataset_id=filter_params['dataset_segmentation'])
            ), Q.AND)


        if 'annotation_exists' in filter_params:
            qs.add((
                Q(annotation__isnull=False)
            ), Q.AND)

        if 'boundingbox_exists' in filter_params:
            qs.add((
                Q(annotationboundingbox__isnull=False)
            ), Q.AND)

        if 'segmentation_exists' in filter_params:
            qs.add((
                Q(annotationsegmentation__isnull=False)
            ), Q.AND)

    
        return Category.objects.filter(qs).distinct().order_by(self.get_sort())