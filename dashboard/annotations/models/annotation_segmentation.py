from django.db import models
from django.contrib.postgres.fields import JSONField

from categories.models import Category
from images.models import Image


class AnnotationSegmentation(models.Model):

    identifier = models.CharField(max_length=256, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    mask = models.TextField(null=True)
    segmentation = JSONField(default=list)

    area = models.FloatField(default=0)
    is_crowd = models.BooleanField(default=False)

    x_min = models.FloatField(null=True)
    x_max = models.FloatField(null=True)
    y_min = models.FloatField(null=True)
    y_max = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)


    def category_name(self):
        return self.category.name
