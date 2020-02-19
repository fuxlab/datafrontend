from django.db import models

from categories.models import Category
from images.models import Image


class AnnotationBoundingbox(models.Model):

    identifier = models.CharField(max_length=256, blank=True, null=True)

    x_min = models.FloatField(null=True)
    x_max = models.FloatField(null=True)
    y_min = models.FloatField(null=True)
    y_max = models.FloatField(null=True)

    area = models.FloatField(default=0)
    is_crowd = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)


    def category_name(self):
        return self.category.name


    def boundingbox_distance(a, b):
        # Brechnung Koordinaten beider Boxen
        xA = max(a['left'], b['left'])
        yA = max(a['top'], b['top'])
        xB = min(a['left'] + a['width'], b['left'] + b['width'])
        yB = min(a['top'] + a['height'], b['top'] + b['height'])

        # Die Schnittmengen beider Flächen.
        area_of_intersection = (xB - xA + 1) * (yB - yA + 1)

        # Flächen beider einzelnen Boundingboxes jeweils
        a_area = (a['width'] + 1) * (a['height'] + 1)
        b_area = (b['width'] + 1) * (b['height'] + 1)

        # Die Fläche beider Boundingboxen zusammengenommen.
        area_of_union = float(a_area + b_area - area_of_intersection)
        distance = area_of_intersection / area_of_union

        return distance