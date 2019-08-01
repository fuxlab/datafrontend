from django.db import models
from django.contrib.postgres.fields import JSONField


class Conflict(models.Model):
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    STATUS_OPEN = 'open'
    STATUS_IGNORE = 'ignore'
    STATUS_SOLVED = 'solved'

    STATUS_CHOICES = (
        (STATUS_OPEN, 'open'),
        (STATUS_IGNORE, 'ignore'),
        (STATUS_SOLVED, 'solved'),
    )
    status     = models.CharField(
        default=STATUS_OPEN,
        max_length=150,
        choices=STATUS_CHOICES,
    )
    
    REASON_IMAGE_DUP = 'image_duplicate'
    REASON_IMAGE_NOTFOUND = 'image_file_not_found'
    REASON_AN_DUP = 'annotation_duplicate'
    REASON_AN_BB_DUP = 'annotation_boundingbox_duplicate'
    REASON_AN_SG_DUP = 'annotation_segmentation_duplicate'

    REASON_CHOICES = (
        (REASON_IMAGE_DUP, 'Duplicate Image'),
        (REASON_IMAGE_NOTFOUND, 'Image Not Found'),
        (REASON_AN_DUP, 'Annotation overlapping'),
        (REASON_AN_BB_DUP, 'Boundingbox overlapping'),
        (REASON_AN_SG_DUP, 'Segmentation overlapping'),
    )
    reason = models.CharField(
        max_length=150,
        choices=REASON_CHOICES,
    )

    message = models.CharField(
        null=True,
        max_length=250,
    )

    affected_ids = JSONField(default=list, null=True, blank=True)


    def __str__(self):
        return str(self.id)
