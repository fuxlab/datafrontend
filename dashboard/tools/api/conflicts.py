from rest_framework import permissions
from rest_framework.response import Response
from django.db.models import Q

from dashboard.lib.api_base import DashboardApiBase

from tools.models import Conflict
from tools.serializers import ConflictSerializer
from tools.tasks.batches import update_images_dataset, update_annotations_category, update_annotation_boundingboxes_category, update_annotation_segmentations_category


class ConflictViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ConflictSerializer


    def get_queryset(self):
        '''
        define queryset
        '''
        qs = Q()     
        filter_params = self.get_filter()

        if 'q' in filter_params:
            qs.add(Q(affected_ids__contains=filter_params['q']), Q.OR)
    
        return Conflict.objects.filter(qs).distinct().order_by(self.get_sort())

