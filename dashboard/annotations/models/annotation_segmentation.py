from django.db import models

from categories.models import Category
from images.models import Image


class AnnotationSegmentation(models.Model):

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    mask = models.TextField(null=True)    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.id


    def category_name(self):
        return self.category.name
