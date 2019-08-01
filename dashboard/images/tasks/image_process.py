import os
from PIL import Image as PImage
from django.db import transaction
from background_task import background
from django.conf import settings

from images.models import Image


def bulk_fetch(max_obj, max_count, fetch_func, start=0):
    counter = start
    while counter < max_count:
        yield fetch_func()[counter:counter + max_obj]
        counter += max_obj


@background(schedule=0)
def update_size():
    fetcher = bulk_fetch(10000, Image.objects.filter(height=0, width=0).count(), lambda: Image.objects.filter(height=0, width=0))
    result = 0
    for bulk in fetcher:
        # bundle db commits
        with transaction.atomic():
            for image in bulk:
                image_full_path = os.path.join(settings.DATAFRONTEND['DATA_PATH'], image.path)
                if os.path.exists(image_full_path):
                    try:
                        img = PImage.open(image_full_path)
                        image.width, image.height = img.size
                        image.save()

                        result += 1
                    except:
                        None
        print('saved();')
    return result

