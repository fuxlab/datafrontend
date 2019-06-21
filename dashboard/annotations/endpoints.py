from django.conf.urls import include, url
from rest_framework import routers

from .api import AnnotationViewSet, AnnotationBoundingboxViewSet, AnnotationSegmentationViewSet

router = routers.DefaultRouter()
router.register('annotations', AnnotationViewSet, basename='annotations')
router.register('annotation-boundingboxes', AnnotationBoundingboxViewSet, basename="annotation-boundingboxes")
router.register('annotation-segmentations', AnnotationSegmentationViewSet, basename="annotation-segmentations")

urlpatterns = [
    url("^", include(router.urls)),
]
