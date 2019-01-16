# Create your views here.
from rest_framework import viewsets, permissions

from .models import Dataset
from .serializers import DatasetSerializer

class DatasetViewSet(viewsets.ModelViewSet):
  queryset = Dataset.objects.all()
  permission_classes = [
    permissions.AllowAny
  ]
  serializer_class = DatasetSerializer