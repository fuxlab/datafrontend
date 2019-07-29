from background_task import background


@background(schedule=0)
def update_images_dataset(params):
    # so some shit
    print('excecuted update_images_dataset')


@background(schedule=0)
def update_annotations_category(params):
    # so some shit
    print('excecuted update_annotations_category')


@background(schedule=0)
def update_annotation_boundingboxes_category(params):
    # so some shit
    print('excecuted update_annotation_boundingboxes_category')


@background(schedule=0)
def update_annotation_segmentations_category(params):
    # so some shit
    print('excecuted update_annotation_segmentations_category')
