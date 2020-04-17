from django.db import models

from datasets.models import Dataset

class Image(models.Model):

    identifier = models.CharField(max_length=256, blank=True, null=True)

    type_id = models.IntegerField(null=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    url = models.CharField(max_length=2048, null=True)
    path = models.CharField(max_length=2048, null=True)
    name = models.CharField(max_length=2048, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    height = models.IntegerField(default=0, null=True)
    width = models.IntegerField(default=0, null=True)


    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)


    def line(self):
        '''
        return one line with basic information for csv export purposes
        '''
        #if self.type is 'image':
        #return [ self.image(), 0, 0, self.uid, self.dataset_id ]
        return [ self.id ]

    
    def image(self):
        '''
        return path to image in full size
        '''
        return '/api/image/%s.png' % (self.id)


    def preview(self):
        '''
        return path to image in preview, thumbnail size
        '''
        return '/api/image/preview/%s.png' % (self.id)        


    def thumbnail(self):
        '''
        return path to image in preview, thumbnail size
        '''
        return '/api/image/thumbnail/%s.png' % (self.id) 


    def types(self):
        
        types = []
        
        for annotation in self.annotation_set.exclude(x_min__isnull=True).all():
            types.append('[ BB ' + str(annotation.category.name)+ ' ]')
        
        for annotation in self.annotation_set.exclude(segmentation__isnull=True).all():
            types.append('[ SG ' + str(annotation.category.name)+ ' ]')
        
        for annotation in self.annotation_set.all():
            types.append('[ AN ' + str(annotation.category.name)+ ' ]')

        return ' '.join(types)

