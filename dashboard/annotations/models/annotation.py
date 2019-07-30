from django.db import models

from categories.models import Category
from images.models import Image


class Annotation(models.Model):
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


    def category_name(self):
        return self.category.name


    def image_name(self):
        return self.image.name