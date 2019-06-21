from rest_framework import permissions
from rest_framework.response import Response
from dashboard.lib.api_base import DashboardApiBase
from .models import Annotation, AnnotationBoundingbox, AnnotationSegmentation
from .serializers import AnnotationSerializer, AnnotationBoundingboxSerializer, AnnotationSegmentationSerializer


class AnnotationViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnotationSerializer


    def get_queryset(self):
        queryset = Annotation.objects.all()
        
        filter_params = self.get_filter()

        if 'image' in filter_params:
            q = Annotation.objects.filter(image=filter_params['image'])
            queryset = queryset & q

        if 'category' in filter_params:
            q = Annotation.objects.filter(category=filter_params['category'])
            queryset = queryset & q

        if 'dataset' in filter_params:
            q = Annotation.objects.filter(image__dataset=filter_params['dataset'])
            queryset = queryset & q


        if 'type' in filter_params:
            filter_types = filter_params['type'].split(',')
            for filter_type in filter_types:
                #if filter_type == 'annotation':
                #    # q = Annotation.objects.filter(category_id=filter_params['category_id'])
                #    # queryset = queryset & q
                if filter_type == 'boundingbox':
                    q = Annotation.objects.exclude(annotationboundingbox=None)
                    queryset = queryset & q
                elif filter_type == 'segmentation':
                    q = Annotation.objects.exclude(annotationsegmentation=None)
                    queryset = queryset & q

    
        return queryset.order_by(self.get_sort())



class AnnotationBoundingboxViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnotationBoundingboxSerializer


    def get_queryset(self):
        queryset = AnnotationBoundingbox.objects.all()

        filter_params = self.get_filter()

        if 'annotation' in filter_params:
            q = AnnotationBoundingbox.objects.filter(annotation=filter_params['annotation'])
            queryset = queryset & q

        return queryset.order_by(self.get_sort())


    def list(self, request):
        # return empty result when annotation is not given for list-views
        filter_params = self.get_filter()
        if 'annotation' not in filter_params:
            return Response([])
        
        return super(AnnotationBoundingboxViewSet, self).list(request)



class AnnotationSegmentationViewSet(DashboardApiBase):

    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AnnotationSegmentationSerializer

    
    def get_queryset(self):
        queryset = AnnotationSegmentation.objects.all()

        filter_params = self.get_filter()

        if 'annotation' in filter_params:
            q = AnnotationSegmentation.objects.filter(annotation=filter_params['annotation'])
            queryset = queryset & q

        return queryset.order_by(self.get_sort())


    def list(self, request):
        # return empty result when annotation is not given for list-views
        filter_params = self.get_filter()
        if 'annotation' not in filter_params:
            return Response([])
        
        return super(AnnotationSegmentationViewSet, self).list(request)
