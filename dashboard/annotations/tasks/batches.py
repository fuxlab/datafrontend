from background_task import background

from annotations.models import Batch, Annotation, AnnotationBoundingbox, AnnotationSegmentation
from images.models import Image

@background(schedule=0)
def update_images_dataset(id):
    batch = Batch.objects.get(id=id)
    result = Image.objects.filter(id__in=batch.params[0]).update(dataset_id=batch.params[1])
    batch.log = [ 'changed %s image datasets to %s' % (result, batch.params[1]) ]
    batch.save
    return result


@background(schedule=0)
def update_annotations_category(id):
    batch = Batch.objects.get(id=id)
    result = Annotation.objects.filter(id__in=batch.params[0]).update(category_id=batch.params[1])
    batch.log = [ 'changed %s annotation categories to %s' % (result, batch.params[1]) ]
    batch.save
    return result


@background(schedule=0)
def update_annotation_boundingboxes_category(id):
    batch = Batch.objects.get(id=id)
    result = AnnotationBoundingbox.objects.filter(id__in=batch.params[0]).update(category_id=batch.params[1])
    batch.log = [ 'changed %s annotation_boundingboxes categories to %s' % (result, batch.params[1]) ]
    batch.save
    return result


@background(schedule=0)
def update_annotation_segmentations_category(id):
    batch = Batch.objects.get(id=id)
    result = AnnotationSegmentation.objects.filter(id__in=batch.params[0]).update(category_id=batch.params[1])
    batch.log = [ 'changed %s annotation_segmentations categories to %s' % (result, batch.params[1]) ]
    batch.save
    return result