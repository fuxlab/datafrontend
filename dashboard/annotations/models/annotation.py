from django.db import models
from django.contrib.postgres.fields import JSONField

from categories.models import Category
from images.models import Image

import itertools
import numpy as np


class AnnotationBoundingboxManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(x_min__isnull=True)


class AnnotationSegmentationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(segmentation__isnull=True)


class Annotation(models.Model):
    
    identifier = models.CharField(max_length=256, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # boundingbox and segmentation
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    area = models.FloatField(default=0)
    is_crowd = models.BooleanField(default=False)

    # only boundingboxes part
    x_min = models.FloatField(null=True)
    x_max = models.FloatField(null=True)
    y_min = models.FloatField(null=True)
    y_max = models.FloatField(null=True)


    # only segmentation part
    mask = models.TextField(null=True)
    segmentation = JSONField(blank=True, null=True)

    # query scopes
    objects = models.Manager()
    boundingbox_objects = AnnotationBoundingboxManager()
    segmentation_objects = AnnotationSegmentationManager()


    def flatten(lst):
        '''
        flatten list of lists of lists
        '''
        result = []
        for i in lst:
            if not isinstance(i, list):
                result.append(i)
            else:
                result.extend(Annotation.flatten(i))
        return result


    def get_coords_from_segmentation(segmentation):
        segmentation = list(Annotation.flatten(segmentation))

        points = np.array_split(segmentation, len(segmentation) / 2)
        x_min = min([point[0] for point in points])
        x_max = max([point[0] for point in points])
        y_min = min([point[1] for point in points])
        y_max = max([point[1] for point in points])

        return (x_min, x_max, y_min, y_max)


    def save(self, *args, **kwargs):

        if self.segmentation and len(self.segmentation) > 0 and type(self.segmentation) is list:
            self.x_min, self.x_max, self.y_min, self.y_max = Annotation.get_coords_from_segmentation(self.segmentation)
            self.height = self.y_max - self.y_min
            self.width = self.x_max - self.x_min
            #self.area = Annotation.area_from_segmentation(self.segmentation)

        elif self.x_min is not None:
            if self.x_max is None and self.x_min is not None and self.width is not None:
                self.x_max = self.x_min + self.width
            else:
                self.width = self.x_max  - self.x_min

            if self.y_max is None and self.y_min is not None and self.height is not None:
                self.y_max = self.y_min + self.height
            else:
                self.height = self.y_max  - self.y_min

        super(Annotation, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.id)


    def types(self):
        '''
        return filles types of annotation
        '''
        types = ['annotation']
        if self.x_min is not None:
            types.append('boundingbox')
        if self.segmentation is not None:
            types.append('segmentation')
        
        return types


    def category_name(self):
        return self.category.name


    def image_name(self):
        return self.image.name


    def boundingbox_distance(a, b):
        '''
        calculate distance between two boundingboxes
        '''
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
