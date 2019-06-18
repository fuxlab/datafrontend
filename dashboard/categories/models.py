from django.db import models

class Category(models.Model):
  
    dataset_id = models.IntegerField(null=True)

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name