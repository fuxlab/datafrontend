from django.db import models
from django.db.models import Count
from django.db.models import Q

from projects.models import Project
from images.models import Image

class Category(models.Model):

    identifier = models.CharField(max_length=256, blank=True, null=True)  
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
            Q(annotation__category_id=self.id)
        )
        
        return q1.distinct().count()


    def annotations_count(self):
        '''
        reuturn count of annotations
        '''
        return self.annotation_set.count()


    def boundingboxes_count(self):
        '''
        reuturn count of boundingboxes
        '''
        return self.annotation_set.filter(~Q(x_min__isnull=True)).count()


    def segmentations_count(self):
        '''
        reuturn count of segmentations
        '''
        return self.annotation_set.filter(~Q(segmentation__isnull=True)).count()


    def quick_name(id):
        '''
        Search for a category and return name, otherwise generate a default with id
        '''
        try:
            category = Category.objects.get(id=id)
            return category.name
        except:
            return 'Category %s' % (id)
