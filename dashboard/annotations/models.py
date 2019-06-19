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

    def image_preview(self):
        return self.image.name

    def types(self):
        # types should always be only one (!)
        types = []
        if self.annotationboundingbox_set.count() > 0:
            types.append('BoundingBox')
        if self.annotationsegmentation_set.count() > 0:
            types.append('Segmentation')
        return ', '.join(types)


class AnnotationBoundingbox(models.Model):

    x_min = models.FloatField(null=True)
    x_max = models.FloatField(null=True)
    y_min = models.FloatField(null=True)
    y_max = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class AnnotationSegmentation(models.Model):

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    mask = models.TextField(null=True)    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
