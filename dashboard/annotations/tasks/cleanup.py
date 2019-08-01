import itertools

from background_task import background
from django.db.models import Count

from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation
from images.models import Image


@background(schedule=0)
def cleanup_annotation_boundingboxes():
    
    # find all images with minimum two boundingboxes in same category
    # query can be improoved that iou-calculation is not needed:
    # add group_by: (x_min, x_max, y_min, y_max)
    bb_results = AnnotationBoundingbox.objects.values('image_id', 'category_id')\
        .annotate(category_id_count=Count('category_id'))\
        .filter(category_id_count__gte=2)

    deleted = []
    for bb in bb_results:
        image = Image.objects.get(id=bb['image_id'])
        potentially_conflicted_bbs = image.annotationboundingbox_set.filter(category_id=bb['category_id']).all()

        # compare each item with the rest
        for a, b in itertools.combinations(potentially_conflicted_bbs, 2):
            distance = AnnotationBoundingbox.boundingbox_distance({
                    'left': a.x_min,
                    'width': a.x_max - a.x_min,
                    'height': a.y_max - a.y_min,
                    'top': image.height - a.y_max,
                }, {
                    'left': b.x_min,
                    'width': b.x_max - b.x_min,
                    'height': b.y_max - b.y_min,
                    'top': image.height - b.y_max,
                })
        
            if distance == 1.0:
                deleted.append(b.id)

    AnnotationBoundingbox.objects.filter(id__in=deleted).delete()

    return len(deleted)