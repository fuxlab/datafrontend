import os
from background_task import background

from datasets.models import Dataset, Folder
from django.conf import settings

from datasets.lib import ImportCoco


@background(schedule=1) # run in one second from now
def import_coco_task(dataset_id, file_name):
    if not int(dataset_id) > 0:
        return False

    dataset = Dataset.objects.get(id=int(dataset_id))
    if not dataset:
        return False

    file_path = os.path.join(settings.DATAFRONTEND['DATA_PATH'], dataset.identifier, str(file_name))

    if os.path.isfile(file_path):
        importer = ImportCoco(dataset)
        if importer.read_file(file_path) is True:
            importer.save()
            return True
    return False
