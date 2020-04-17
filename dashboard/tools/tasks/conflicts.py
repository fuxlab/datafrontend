import itertools

from background_task import background
from django.db.models import Count

from tools.models import Conflict
from annotations.models import Annotation
from images.models import Image

from django.db.models import Q

@background(schedule=0)
def create_annotation_boundingbox_conflicts(threshold=0.9):
    
    # find all images with minimum two boundingboxes in same category
    bb_results = Annotation.boundingbox_objects.values('image_id', 'category_id')\
        .annotate(category_id_count=Count('category_id'))\
        .filter(category_id_count__gte=2)

    for bb in bb_results:
        image = Image.objects.get(id=bb['image_id'])
        potentially_conflicted_bbs = image.annotation_set.filter(
            Q(category_id=bb['category_id']) &
            ~Q(x_min__isnull=True)
        ).all()

        # compare each item with the rest
        for a, b in itertools.combinations(potentially_conflicted_bbs, 2):
            distance = Annotation.boundingbox_distance({
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
            
            if distance >= threshold:
                conflict = Conflict.objects.create(
                    reason=Conflict.REASON_AN_BB_DUP,
                    affected_ids=[a.id, b.id],
                    message=('overlapping distance %s is greater than %s.' % (distance, threshold))
                )
