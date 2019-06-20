from django.db import models

from datasets.models import Dataset

class Image(models.Model):
  
    type_id = models.IntegerField(null=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def types(self):
        # types should always be only one (!)
        types = []
        if self.annotation_set.count() > 0:
            for annotation in self.annotation_set.all():
                name = annotation.category_name()
                if annotation.annotationboundingbox_set.count() > 0:
                    types.append('[ ' + name + ': BoundingBox ]')
                if annotation.annotationsegmentation_set.count() > 0:
                    types.append('[' + name + ': Segmentation ]')
        
        return ' '.join(types)
