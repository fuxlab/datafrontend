from django.db import models
from projects.models import Project
from images.models import Image

class Category(models.Model):
  
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    def images_count(self):
        '''
        return counf of distinct images
        '''
        q1 = Image.objects.filter(annotation__category_id=self.id)
        q2 = Image.objects.filter(annotationboundingbox__category_id=self.id)
        q3 = Image.objects.filter(annotationsegmentation__category_id=self.id)
        q = q1 & q2 & q3

        return q.distinct().count()


    def annotations_count(self):
        '''
        reuturn count of annotations
        '''
        return self.annotation_set.count()


    def boundingboxes_count(self):
        '''
        reuturn count of boundingboxes
        '''
        return self.annotationboundingbox_set.count()


    def segmentations_count(self):
        '''
        reuturn count of segmentations
        '''
        return self.annotationsegmentation_set.count()
