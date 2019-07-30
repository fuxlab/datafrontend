from django.db import models
from django.contrib.postgres.fields import JSONField

class Batch(models.Model):
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    action     = models.CharField(max_length=2048, null=True)
    params     = JSONField(default=list, null=True, blank=True)
    log        = JSONField(default=list, null=True, blank=True)

    status     = models.CharField(default='pending', max_length=50, null=True)


    def __str__(self):
        return self.id


    def params_list(self, index):
        '''
        get a value from params and be sure it is a list
        '''
        if isinstance(self.params[index], str):
            return [x.strip() for x in self.params[index].split(',')]
        if isinstance(self.params[index], list):
            return self.params[index]
        return []


    def params_int(self, index):
        '''
        get a value from params and be sure it is an int
        '''
        if isinstance(self.params[index], int):
            return self.params[index]
        if self.params[index] and self.params[index] != '' and len(self.params[index]) > 0:
            return int(self.params[index])
        return 0
