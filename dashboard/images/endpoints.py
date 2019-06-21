from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from .api import ImageViewSet
from .image import ImagePreview

router = routers.DefaultRouter()
router.register('images', ImageViewSet, basename='images')

urlpatterns = [
    url("^", include(router.urls)),
    path('image/<int:image_id>.png', ImagePreview.as_view())
]