from django.conf.urls import include, url
from rest_framework import routers

from tools.api import BatchViewSet

router = routers.DefaultRouter()
router.register('batches', BatchViewSet, basename='batches')

urlpatterns = [
    url("^", include(router.urls)),
]
