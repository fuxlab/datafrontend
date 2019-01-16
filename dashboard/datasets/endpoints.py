from django.conf.urls import include, url
from rest_framework import routers

from .api import DatasetViewSet

router = routers.DefaultRouter()
router.register('datasets', DatasetViewSet)

urlpatterns = [
  url("^", include(router.urls)),
]