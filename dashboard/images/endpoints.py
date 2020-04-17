from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from .api import ImageViewSet, ImageExport

from images.renderers import PNGRenderer, JPGImageRenderer, ImageRenderer


router = routers.DefaultRouter()
router.register('images', ImageViewSet, basename='images')

urlpatterns = [
    path('images/export/download', ImageExport.as_view({'get': 'download'})),
    path('images/export/', ImageExport.as_view({'get': 'list'})),
    
    url("^", include(router.urls)),
    # png images
    path('image/boundingbox_<int:id>.png', ImageRenderer.as_view({'get': 'boundingbox_crop'})),
    path('image/segmentation_<int:id>.png', ImageRenderer.as_view({'get': 'segmentation_crop'})),
    path('image/plot.png', ImageRenderer.as_view({'get': 'plot'})),
    path('image/thumbnail/<int:id>.png', ImageRenderer.as_view({'get': 'thumbnail'})),
    path('image/preview/<int:id>.png', ImageRenderer.as_view({'get': 'preview'})),
    path('image/<int:id>.png', ImageRenderer.as_view({'get': 'original'})),
    
    # jpg images
    path('image/boundingbox_<int:id>.jpg', JPGImageRenderer.as_view({'get': 'boundingbox_crop'})),
    path('image/segmentation_<int:id>.jpg', JPGImageRenderer.as_view({'get': 'segmentation_crop'})),
    path('image/plot.jpg', JPGImageRenderer.as_view({'get': 'plot'})),
    path('image/thumbnail/<int:id>.jpg', JPGImageRenderer.as_view({'get': 'thumbnail'})),
    path('image/preview/<int:id>.jpg', JPGImageRenderer.as_view({'get': 'preview'})),
    path('image/preview/<int:id>.svg', JPGImageRenderer.as_view({'get': 'svg_segmentation'})),
    path('image/<int:id>.jpg', JPGImageRenderer.as_view({'get': 'original'})),
]