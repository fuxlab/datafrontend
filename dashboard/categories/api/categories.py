from rest_framework import viewsets, permissions
from dashboard.lib.api_base import DashboardApiBase
from django.db.models import Q

from categories.models import Category
from categories.serializers import CategorySerializer


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
            qs.add(Q(annotation__image__dataset_id=filter_params['dataset_annotation']), Q.AND)

        if 'dataset_boundingbox' in filter_params:
            qs.add((
                Q(annotation__image__dataset_id=filter_params['dataset_boundingbox']) &
                ~Q(annotation__x_min__isnull=True)
            ), Q.AND)

        if 'dataset_segmentation' in filter_params:
            qs.add((
                Q(annotation__image__dataset_id=filter_params['dataset_segmentation']) &
                ~Q(annotation__segmentation__isnull=True)
            ), Q.AND)

        if 'annotation_exists' in filter_params:
            qs.add(~Q(annotation__isnull=True), Q.AND)

        if 'boundingbox_exists' in filter_params:
            qs.add(~Q(annotation__x_min__isnull=True), Q.AND)

        if 'segmentation_exists' in filter_params:
            qs.add(~Q(annotation__segmentation__isnull=True), Q.AND)

        return Category.objects.filter(qs).order_by(self.get_sort())
