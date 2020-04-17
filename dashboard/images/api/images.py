from rest_framework import permissions
from dashboard.lib.api_base import DashboardApiBase
from images.models import Image
from images.serializers.image import ImageSerializer
from django.db.models import Q


class ImageViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ImageSerializer


    def get_queryset(self):
        '''
        define queryset
        '''
        q_objects = Q()

        filter_params = self.get_filter()
        if 'dataset' in filter_params:
            q_objects.add(Q(dataset=filter_params['dataset']), Q.AND)

        if 'annotation' in filter_params:
            q_objects.add(
                Q(annotation__category=filter_params['annotation'])
            , Q.AND)

        if 'boundingbox' in filter_params:
            q_objects.add(
                Q(annotation__category=filter_params['boundingbox']) &
                ~Q(annotation__x_min__isnull=True)
            , Q.AND)

        if 'segmentation' in filter_params:
            q_objects.add(
                Q(annotation__category=filter_params['segmentation']) &
                ~Q(annotation__segmentation__isnull=True)
            , Q.AND)

        if 'q' in filter_params:
            q_objects.add((
                Q(name__contains=filter_params['q']) | Q(url__contains=filter_params['q'])
            ), Q.AND)
            
        if len(q_objects) > 0:
            return Image.objects.filter(q_objects).order_by(self.get_sort()).distinct()
        else:
            return Image.objects.filter(q_objects).order_by(self.get_sort()).distinct()
