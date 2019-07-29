from django.db import models
from django.contrib.postgres.fields import JSONField

class Batch(models.Model):
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    action     = models.CharField(max_length=2048, null=True)
    params     = JSONField(default=list, null=True, blank=True)
    log        = JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return self.id
