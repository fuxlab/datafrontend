import os
from background_task import background

from datasets.models import Dataset, Folder
from django.conf import settings

from images.models import Image

@background(schedule=1) # run in one second from now
def init_folder_task(dataset_id):
    # print(dataset_id)

    if not int(dataset_id) > 0:
        return False

    dataset = Dataset.objects.get(id=int(dataset_id))
    if not dataset:
        return False

    path = os.path.join(settings.DATAFRONTEND['DATA_PATH'], dataset.identifier)
    files = Folder.files(path)

    for file_name in files:
        Image.objects.create(name=file_name, path=os.path.join(dataset.identifier, file_name), dataset_id=int(dataset_id))
