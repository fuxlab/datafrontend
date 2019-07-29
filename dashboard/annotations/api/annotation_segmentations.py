from rest_framework import permissions
from rest_framework.response import Response
from django.db.models import Q

from dashboard.lib.api_base import DashboardApiBase
from annotations.models import AnnotationSegmentation
from annotations.serializers import AnnotationSegmentationSerializer


class AnnotationSegmentationViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnotationSegmentationSerializer

    
    def get_queryset(self):
        qs = Q()
        filter_params = self.get_filter()

        if 'image' in filter_params:
            qs.add(Q(image=filter_params['image']), Q.AND)

        return AnnotationSegmentation.objects.filter(qs).distinct().order_by(self.get_sort())

