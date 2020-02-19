from django.conf.urls import include, url
from rest_framework import routers

from .api import DatasetViewSet, FolderView, ImportFilesView

router = routers.DefaultRouter()
router.register('datasets', DatasetViewSet, basename='datasets')

urlpatterns = [
    url(r'^datasets/import_files/$', ImportFilesView.as_view()),
    url(r'^folders/$', FolderView.as_view()),
    url("^", include(router.urls)),
]