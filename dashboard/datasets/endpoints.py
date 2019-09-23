from django.conf.urls import include, url
from rest_framework import routers

from .api import DatasetViewSet, FolderView

router = routers.DefaultRouter()
router.register('datasets', DatasetViewSet, basename='datasets')

urlpatterns = [
    url(r'^folders/$', FolderView.as_view()),
    url("^", include(router.urls)),
]