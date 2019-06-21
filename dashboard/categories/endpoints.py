from django.conf.urls import include, url
from rest_framework import routers

from .api import CategoryViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    url("^", include(router.urls)),
]