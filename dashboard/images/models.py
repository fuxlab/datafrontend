from django.db import models

class Image(models.Model):
  
    dataset_id = models.IntegerField(null=True)
    type_id = models.IntegerField(null=True)

    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name