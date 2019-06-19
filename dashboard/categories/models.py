from django.db import models
from datasets.models import Dataset

class Category(models.Model):
  
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    def __str__(self):
        return self.name