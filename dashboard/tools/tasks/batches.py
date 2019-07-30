from background_task import background

from tools.models import Batch
from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation
from images.models import Image

@background(schedule=0)
def update_images_dataset(batch_id):
    batch = Batch.objects.get(id=int(batch_id))
    batch.status = 'running'
    batch.save()

    result = Image.objects.filter(id__in=batch.params_list(0)).update(dataset_id=batch.params_int(1))
    
    batch.log = [ 'changed %s image datasets to %s' % (result, batch.params_int(1)) ]
    batch.status = 'finished'
    batch.save()
    return result


@background(schedule=0)
def update_annotations_category(batch_id):
    batch = Batch.objects.get(id=int(batch_id))
    batch.status = 'running'
    batch.save()

    result = Annotation.objects.filter(id__in=batch.params_list(0)).update(category_id=batch.params_int(1))
    
    batch.log = [ 'changed %s annotation categories to %s' % (result, batch.params_int(1)) ]
    batch.status = 'finished'
    batch.save()
    return result


@background(schedule=0)
def update_annotation_boundingboxes_category(batch_id):
    batch = Batch.objects.get(id=int(batch_id))
    batch.status = 'running'
    batch.save()

    result = AnnotationBoundingbox.objects.filter(id__in=batch.params_list(0)).update(category_id=batch.params_int(1))
    
    batch.log = [ 'changed %s annotation_boundingboxes categories to %s' % (result, batch.params_int(1)) ]
    batch.status = 'finished'
    batch.save()
    return result


@background(schedule=0)
def update_annotation_segmentations_category(batch_id):
    batch = Batch.objects.get(id=int(batch_id))
    batch.status = 'running'
    batch.save()

    result = AnnotationSegmentation.objects.filter(id__in=batch.params_list(0)).update(category_id=batch.params_int(1))

    batch.log = [ 'changed %s annotation_segmentations categories to %s' % (result, batch.params_int(1)) ]
    batch.status = 'finished'
    batch.save()
    return result