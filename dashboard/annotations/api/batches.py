from rest_framework import permissions
from rest_framework.response import Response
from django.db.models import Q

from dashboard.lib.api_base import DashboardApiBase
from annotations.models import Batch
from annotations.serializers import BatchSerializer

from annotations.tasks.batches import update_images_dataset, update_annotations_category, update_annotation_boundingboxes_category, update_annotation_segmentations_category

class BatchViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = BatchSerializer


    def get_queryset(self):
        '''
        define queryset
        '''
        qs = Q()     
        filter_params = self.get_filter()

        if 'q' in filter_params:
            qs.add(Q(log__contains=filter_params['q']), Q.OR)
            ps.add(Q(params__contains=filter_params['q']), Q.OR)
    
        return Batch.objects.filter(qs).distinct().order_by(self.get_sort())

    
    def perform_create(self, serializer):
        '''
        save queue
        '''
        serializer.save()
        if serializer.data['action'] == 'update_images_dataset':
            update_images_dataset(serializer.data['params'])
        elif serializer.data['action'] == 'update_annotations_category':
            print('update_annotations_category')
            update_annotations_category(serializer.data['params'])
        elif serializer.data['action'] == 'update_annotation_boundingboxes_category':
            update_annotation_boundingboxes_category(serializer.data['params'])
        elif serializer.data['action'] == 'update_annotation_segmentations_category':
            update_annotation_segmentations_category(serializer.data['params'])