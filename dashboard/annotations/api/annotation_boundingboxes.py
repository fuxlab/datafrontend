from rest_framework import permissions
from rest_framework.response import Response
from django.db.models import Q

from dashboard.lib.api_base import DashboardApiBase
from annotations.models import Annotation
from annotations.serializers import AnnotationBoundingboxSerializer


class AnnotationBoundingboxViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnotationBoundingboxSerializer


    def get_queryset(self):
        qs = Q()
        filter_params = self.get_filter()

        if 'image' in filter_params:
            qs.add(Q(image=filter_params['image']), Q.AND)

        return Annotation.boundingbox_objects.filter(qs).distinct().order_by(self.get_sort())
