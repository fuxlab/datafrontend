from django.db import models
from projects.models import Project

class Dataset(models.Model):
  
    identifier = models.SlugField(null=True)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    def images_count(self):
        return self.image_set.count()