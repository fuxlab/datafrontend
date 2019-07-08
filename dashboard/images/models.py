from django.db import models

from datasets.models import Dataset

class Image(models.Model):
  
    type_id = models.IntegerField(null=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    url = models.CharField(max_length=2048, null=True)
    path = models.CharField(max_length=2048, null=True)
    name = models.CharField(max_length=2048, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def line(self):
        '''
        return one line with basic information for csv export purposes
        '''
        #if self.type is 'image':
        #return [ self.image(), 0, 0, self.uid, self.dataset_id ]
        print(self)
        return [ self.id ]

    
    def image(self):
        return '/api/image/%s.png' % (self.id)


    def types(self):
        
        types = []
        
        for annotation in self.annotationboundingbox_set.all():
            types.append('[ BB ' + str(annotation.category.name)+ ' ]')
        
        for annotation in self.annotationsegmentation_set.all():
            types.append('[ SG ' + str(annotation.category.name)+ ' ]')
        
        for annotation in self.annotation_set.all():
            types.append('[ AN ' + str(annotation.category.name)+ ' ]')

        return ' '.join(types)
