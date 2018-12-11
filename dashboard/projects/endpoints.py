from django.conf.urls import include, url
from rest_framework import routers

from .api import ProjectViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)

urlpatterns = [
  url("^", include(router.urls)),
]