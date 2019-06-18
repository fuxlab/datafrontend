from django.db import models

class Annotation(models.Model):
  
    image_id = models.IntegerField(null=True)
    category_id = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id