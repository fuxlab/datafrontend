from django.conf.urls import include, url
from rest_framework import routers

from .api import ImageViewSet

router = routers.DefaultRouter()
router.register('images', ImageViewSet, basename='images')

urlpatterns = [
    url("^", include(router.urls)),
]