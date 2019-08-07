from django.db import models
from django.db.models import Count
from django.db.models import Q


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
        use wisly, might be slow
        '''
        q1 = Image.objects.filter(
            Q(annotation__category_id=self.id) & 
            Q(annotationboundingbox__category_id=self.id) &
            Q(annotationsegmentation__category_id=self.id)
        )
        
        return q1.count()


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

    def quick_name(id):
        try:
            category = Category.objects.get(id=id)
            return category.name
        except:
            return 'Category %s' % (id)