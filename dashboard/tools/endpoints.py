from django.conf.urls import include, url
from rest_framework import routers

from tools.api import BatchViewSet, ConflictViewSet

router = routers.DefaultRouter()
router.register('batches', BatchViewSet, basename='batches')
router.register('conflicts', ConflictViewSet, basename='conflicts')

urlpatterns = [
    url("^", include(router.urls)),
]
