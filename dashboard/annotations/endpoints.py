from django.conf.urls import include, url
from rest_framework import routers

from .api import AnnotationViewSet

router = routers.DefaultRouter()
router.register('annotations', AnnotationViewSet, basename='annotations')

urlpatterns = [
    url("^", include(router.urls)),
]