from django.db import models
from projects.models import Project

from django.utils.text import slugify

class Dataset(models.Model):
  
    identifier = models.SlugField(null=True)
    version = models.CharField(max_length=16, blank=True)

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048, blank=True)

    contributor = models.CharField(max_length=2048, blank=True)
    url = models.CharField(max_length=1042, blank=True)
    release_date = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.identifier is None or len(self.identifier) == 0:
                self.identifier = self.name
            self.identifier = slugify(self.identifier)

        super(Dataset, self).save(*args, **kwargs)

    def path(self):
        '''
        path of dataset
        '''
        

    def images_count(self):
        '''
        return database count of images
        '''
        
        return self.image_set.count()

        
    def quick_name(id):
        '''
        Search for a dataset and return name, otherwise generate a default with id
        '''
        try:
            dataset = Dataset.objects.get(id=id)
            return dataset.name
        except:
            return 'Dataset %s' % (id)
