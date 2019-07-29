from rest_framework import permissions
from rest_framework.response import Response
from django.db.models import Q

from dashboard.lib.api_base import DashboardApiBase
from annotations.models import Annotation
from annotations.serializers import AnnotationSerializer


class AnnotationViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnotationSerializer


    def get_queryset(self):
        qs = Q()
        filter_params = self.get_filter()
            
        if 'image' in filter_params:
            qs.add(Q(image=filter_params['image']), Q.AND)

        if 'category' in filter_params:
            qs.add(Q(category=filter_params['category']), Q.AND)

        if 'dataset' in filter_params:
            qs.add(Q(image__dataset=filter_params['dataset']), Q.AND)

        return Annotation.objects.filter(qs).distinct().order_by(self.get_sort())